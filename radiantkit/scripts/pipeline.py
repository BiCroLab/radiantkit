import argparse
import os

from radiantkit import argtools as ap


def init_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    parser = subparsers.add_parser(
        __name__.split(".")[-1],
        description="Long description",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Setup vanilla snakemake workflows. *NOT IMPLEMENTED*",
    )

    parser.add_argument(
        "workflow",
        metavar="name",
        type=str,
        choices=["yfish"],
        help="""Name of the workflow. Available: yfish""",
    )
    parser.add_argument(
        "root", type=str, help="""Path to folder where to set up the workflow."""
    )

    parser.add_argument(
        "--conda-env",
        type=str,
        metavar="STRING",
        help="""Name of the
        conda environment where radiantkit is installed to.""",
    )
    parser.add_argument(
        "--shell-type",
        type=str,
        metavar="STRING",
        help="""Shell type where to run snakemake. One of: bash, zsh.""",
    )

    parser.add_argument(
        "-f",
        action="store_const",
        help="""Overwrite existing folder.""",
        const=True,
        default=False,
    )

    parser = ap.add_version_argument(parser)
    parser.set_defaults(parse=parse_arguments, run=run)

    return parser


def parse_arguments(args: argparse.Namespace) -> argparse.Namespace:
    assert not os.path.isfile(args.root), "cannot create workflow folder"
    assert not os.path.isdir(args.root) or args.f, "workflow folder already exists"
    if not os.path.isdir(args.root):
        os.mkdir(args.root)
    return args


def run(args: argparse.Namespace) -> None:
    raise NotImplementedError
    # setup_workflow(args.root, args.workflow)
    print(f"\nPipeline set up in '{args.root}'.\nNext:\n")
    config_path = os.path.join(args.root, f"{args.workflow}.config.yaml")
    print("(1) Manually update the config file, for example with:")
    print(f"nano '{config_path}'\n")
    print("(2) Then, run the pipeline with:")
    print(f"{os.path.join(args.root, 'run.sh')}\n")
