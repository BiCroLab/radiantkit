""" This is the command line entry point

Accessed both by
$ pip install .
$ python -m radiantkit

and by

$ pipx install .
$ radiantkit
"""

# PEP 690 ..
# import importlib
# importlib.set_lazy_imports()

import sys
import argparse

import radiantkit as rk
import radiantkit.scripts as rks

def default_parser(*args) -> None:
    print(f"radiantkit version {rk.__version__}")
    print(f"Use -h to see the help")
    sys.exit()

def radiant():
    parser = argparse.ArgumentParser(
        description=f"""
Version:    {rk.__version__}
Author:     Gabriele Girelli, et al.
Docs:       http://BiCroLab.github.io/radiantkit
Code:       http://github.com/BiCroLab/radiantkit

Radial Image Analysis Toolkit (RadIAnTkit) is a Python package
for analysis of YFISH of the GPSeq pipeline.  """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(parse=default_parser)
    parser.add_argument(
        "--version", action="version", version=f"{sys.argv[0]} {rk.__version__}"
    )

    subparsers = parser.add_subparsers(
        title="sub-commands",
        help="Access the help page for a sub-command with: sub-command -h",
    )

    rks.czi_to_tiff.init_parser(subparsers)
    rks.nd2_to_tiff.init_parser(subparsers)

    rks.select_nuclei.init_parser(subparsers)
    rks.export_objects.init_parser(subparsers)
    rks.measure_objects.init_parser(subparsers)

    rks.radial_population.init_parser(subparsers)
    rks.radial_object.init_parser(subparsers)
    rks.radial_trajectory.init_parser(subparsers)
    rks.radial_points.init_parser(subparsers)

    rks.tiff_findoof.init_parser(subparsers)
    rks.tiff_segment.init_parser(subparsers)
    rks.tiff_desplit.init_parser(subparsers)
    rks.tiff_split.init_parser(subparsers)
    rks.tiffcu.init_parser(subparsers)

    rks.pipeline.init_parser(subparsers)
    rks.report.init_parser(subparsers)

    # argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args = args.parse(args)
    args.run(args)
