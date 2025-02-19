"""
@author: Gabriele Girelli
@contact: gigi.ga90@gmail.com
"""

import argparse
import logging
import numpy as np  # type: ignore
import os
import re
from rich.progress import track  # type: ignore
import sys
from typing import Iterable, List, Tuple, Union


from .. import argtools as ap

from radiantkit.exception import enable_rich_exceptions
import radiantkit.image as imt
from radiantkit.io import add_log_file_handler
from radiantkit.rkstring import MultiRange
from radiantkit.rkstring import TIFFNameTemplateFields as TNTFields
from radiantkit.rkstring import TIFFNameTemplate as TNTemplate

from radiantkit.conversion import CziFile2

def init_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        __name__.split(".")[-1],
        description=f"""
Convert one or more czi files into single channel tiff images. You can specify multiple
czi files, or multiple folders containing czi files, by separating them with a space.
When a folder is specified as input, all files matching the "inreg" regular expression
are converted. You can change the regular expression to convert a specific files subset.

# File naming

The output tiff file names follow the specified template (-T). A template is a string
including a series of "seeds" that are replaced by the corresponding values when writing
the output file. Available seeds are:
{TNTFields.CHANNEL_NAME} : channel name, lower-cased.
{TNTFields.CHANNEL_ID} : channel ID (number).
{TNTFields.SERIES_ID} : series ID (number).
{TNTFields.DIMENSIONS} : number of dimensions, followed by "D".
{TNTFields.AXES_ORDER} : axes order (e.g., "TZYX").
Leading 0s are added up to 3 digits to any ID seed.

The default template is "{TNTFields.CHANNEL_NAME}_{TNTFields.SERIES_ID}". Hence, when
writing the 3rd series of the "a488" channel, the output file name would be:
"a488_003.tiff".

Please, remember to escape the "$" when running from command line if using double
quotes, i.e., "\\$". Alternatively, use single quotes, i.e., '$'.""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Convert a czi file into single channel tiff images.",
    )

    parser.add_argument(
        "input",
        type=str,
        nargs="+",
        help="""Path a czi file to convert, or to a folder containing czi files.
        To specify multiple inputs, separate them with a space.""",
    )

    parser.add_argument(
        "--outdir",
        metavar="DIRPATH",
        type=str,
        help="""Path to output TIFF folder. Defaults to the input file
        basename. This is ignored when input is a folder.""",
        default=None,
    )
    parser.add_argument(
        "--fields",
        metavar="STRING",
        type=str,
        help="""Convert only fields of view specified as when printing a set
        of pages. Omit if all fields should be converted. E.g., '1-2,5,8-9'.""",
        default=None,
    )
    parser.add_argument(
        "--channels",
        metavar="STRING",
        type=str,
        help="""Convert only specified channels. Specified as space-separated
        channel names. Omit if all channels should be converted.
        E.g., 'dapi cy5 a488'.""",
        default=None,
        nargs="+",
    )

    advanced = parser.add_argument_group("advanced arguments")
    default_inreg = r"^.*\.czi$"
    advanced.add_argument(
        "--inreg",
        type=str,
        metavar="REGEXP",
        help=f"""Regular expression to identify input CZI images.
        Default: '{default_inreg}'""",
        default=default_inreg,
    )
    advanced.add_argument(
        "--template",
        metavar="STRING",
        type=str,
        help=f"""Template for output file name. See main description for more
        details. Default: '{TNTFields.CHANNEL_NAME}_{TNTFields.SERIES_ID}'""",
        default=f"{TNTFields.CHANNEL_NAME}_{TNTFields.SERIES_ID}",
    )
    advanced.add_argument(
        "--compressed",
        action="store_const",
        dest="doCompress",
        const=True,
        default=False,
        help="""Write compressed TIFF as output. Useful especially for binary or
        low-depth (e.g. labeled) images.""",
    )
    advanced.add_argument(
        "-i",
        "--info",
        action="store_const",
        dest="info",
        const=True,
        default=False,
        help="Show details of input nd2 files and stop (nothing is converted).",
    )
    advanced.add_argument(
        "-l",
        "--list",
        action="store_const",
        dest="list",
        const=True,
        default=False,
        help="List input nd2 files and stop (nothing is converted).",
    )

    parser = ap.add_version_argument(parser)
    parser.set_defaults(parse=parse_arguments, run=run)

    return parser



def parse_arguments(args: argparse.Namespace) -> argparse.Namespace:
    if args.fields is not None:
        args.fields = MultiRange(args.fields)

    if args.channels is not None:
        args.channels = [c.lower() for c in args.channels]

    assert 0 != len(args.template)
    args.template = TNTemplate(args.template)

    return args


def check_channels(channels: List[str], czi_image: CziFile2) -> List[str]:
    if channels is None:
        channels = list(czi_image.get_channel_names())
    else:
        channels = czi_image.select_channels(channels)
        if 0 == len(channels):
            logging.error("None of the specified channels was found.")
            sys.exit()
        logging.info(f"Converting only the following channels: {channels}")
    return channels


def field_generator(
    args: argparse.Namespace, czi_image: CziFile2
) -> Iterable[Tuple[np.ndarray, str]]:
    for field_id in args.fields:
        if field_id - 1 >= czi_image.field_count():
            logging.warning(
                "".join(
                    [
                        f"Skipped field #{field_id} ",
                        "(from specified field range, ",
                        "not available in czi file).",
                    ]
                )
            )
            continue
        for yieldedValue in czi_image.get_channel_pixels(args, field_id - 1):
            channel_pixels, channel_id = yieldedValue
            if not list(czi_image.get_channel_names())[channel_id] in args.channels:
                continue
            yield (
                channel_pixels,
                czi_image.get_tiff_path(args.template, channel_id, field_id - 1),
            )


def convert_to_tiff(args: argparse.Namespace, outdir: str, czi_image: CziFile2) -> None:
    export_total = float("inf")
    if args.fields is not None and args.channels is not None:
        export_total = len(args.fields) * len(args.channels)
    elif args.fields is not None:
        export_total = len(args.fields)
    elif args.channels is not None:
        export_total = len(args.channels)
    export_total = min(
        czi_image.field_count() * czi_image.channel_count(), export_total
    )
    for (OI, opath) in track(field_generator(args, czi_image), total=int(export_total)):
        imt.save_tiff(
            os.path.join(outdir, opath),
            OI.astype(imt.get_dtype(int(OI.max()))),
            args.doCompress,
            resolution=(
                1e-6 / czi_image.get_axis_resolution("X"),
                1e-6 / czi_image.get_axis_resolution("Y"),
            ),
            inMicrons=True,
            z_resolution=czi_image.get_axis_resolution("Z") * 1e6,
        )


def check_argument_compatibility(
    args: argparse.Namespace, czi_image: CziFile2
) -> argparse.Namespace:
    assert args.template.can_export_fields(
        czi_image.field_count(), args.fields
    ), "".join(
        [
            "when exporting more than 1 field, the template ",
            f"must include the {TNTFields.SERIES_ID} seed. ",
            f"Got '{args.template.template}' instead.",
        ]
    )

    args.channels = check_channels(args.channels, czi_image)

    assert args.template.can_export_channels(
        czi_image.channel_count(), args.channels
    ), "".join(
        [
            "when exporting more than 1 channel, the template ",
            f"must include either {TNTFields.CHANNEL_ID} or ",
            f"{TNTFields.CHANNEL_NAME} seeds. ",
            f"Got '{args.template.template}' instead.",
        ]
    )

    if args.fields is None:
        args.fields = range(czi_image.field_count())

    return args


def mk_outdir(outdir: Union[str, None], path: str) -> str:
    if outdir is None:
        outdir = os.path.splitext(os.path.basename(path))[0]
        outdir = os.path.join(os.path.dirname(path), outdir)
    assert not os.path.isfile(outdir), f"output directory cannot be a file: {outdir}"
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    return outdir


def convert_single_czi_file(args: argparse.Namespace, path: str, outdir: str = None):
    logging.info(f"Working on file '{path}'.")
    assert os.path.isfile(path), f"input file not found: {path}"
    if args.list:
        return

    czi_image = CziFile2(path)
    if args.info:
        czi_image.log_details()
        logging.info("")
        sys.exit()

    outdir = mk_outdir(outdir, path)
    add_log_file_handler(os.path.join(outdir, "czi_to_tiff.log.txt"))

    czi_image.log_details()
    args = check_argument_compatibility(args, czi_image)
    assert not czi_image.isLive(), "time-course conversion images not implemented."

    logging.info(f"Output directory: '{outdir}'")
    czi_image.squeeze_axes("STCZYX")
    czi_image.reorder_axes("STCZYX")

    if args.fields is not None:
        args.fields = list(args.fields)
        logging.info(
            "Converting only the following fields: " + f"{[x for x in args.fields]}"
        )

    convert_to_tiff(args, outdir, czi_image)


def convert_folder_czi_files(args: argparse.Namespace, path: str):
    assert os.path.isdir(path)
    for fpath in sorted(os.listdir(path)):
        if re.match(args.inreg, fpath) is not None:
            fpath = os.path.join(path, fpath)
            convert_single_czi_file(args, fpath)



def run(args: argparse.Namespace) -> None:
    logging.info(f"Input: {args.input}")
    for input_path in args.input:
        if os.path.isdir(input_path):
            convert_folder_czi_files(args, input_path)
        else:
            convert_single_czi_file(args, input_path, args.outdir)
        logging.info("Done. :thumbs_up: :smiley:")
