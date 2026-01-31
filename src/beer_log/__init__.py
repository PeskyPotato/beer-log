import argparse
from .main import process_checkins


def handle_process_checkins(args):
    kwargs = {}
    if args.templates_dir is not None:
        kwargs['templates_dir'] = args.templates_dir
    if args.content_dir is not None:
        kwargs['content_dir'] = args.content_dir
    
    process_checkins(**kwargs)

def entry():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command", required=True)

    process_checkins_parser = subparser.add_parser("process_checkins")
    process_checkins_parser.add_argument(
        "--templates_dir",
        help="Location of template directory to replace the included defaults."
    )
    process_checkins_parser.add_argument(
        "--content_dir",
        help="Location of content to replace the default ./content/beer"
    )
    process_checkins_parser.set_defaults(func=handle_process_checkins)

    args = parser.parse_args()
    args.func(args)

