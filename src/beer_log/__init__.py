import argparse
from .main import BeerLog, Checkin


def handle_checkin_add(args):
    kwargs = {}
    if args.brewery is not None:
        kwargs['brewery_name'] = args.brewery
    if args.beer is not None:
        kwargs['beer_name'] = args.beer
    if args.content_dir is not None:
        kwargs['content_dir'] = args.content_dir

    checkin = Checkin(**kwargs)
    checkin.add_checkin()


def handle_checkin_process(args):
    kwargs = {}
    if args.content_dir is not None:
        kwargs['content_dir'] = args.content_dir
    if args.templates_dir is not None:
        kwargs['templates_dir'] = args.templates_dir
    if args.output_dir is not None:
        kwargs['output_dir'] = args.output_dir
    if args.prefix is not None:
        kwargs['prefix'] = args.prefix
    if args.base_url is not None:
        kwargs['base_url'] = args.base_url

    bl = BeerLog(**kwargs)
    bl.process_checkins()


def entry():
    parser = argparse.ArgumentParser()
    namepspace_parser = parser.add_subparsers(dest="command", required=True)

    # Namespace: checkin
    checkin_parser = namepspace_parser.add_parser("checkin")
    checkin_action_parser = checkin_parser.add_subparsers(dest="command", required=True)

    # Action: process
    checkin_process_parser = checkin_action_parser.add_parser("process")
    checkin_process_parser.add_argument(
        "--content_dir",
        help="Location of content to replace the default ./content/beer"
    )
    checkin_process_parser.add_argument(
        "--templates_dir",
        help="Location of template directory to replace the included defaults."
    )
    checkin_process_parser.add_argument(
        "--output_dir",
        help="Location of rendered HTML files to replace the default ./beer"
    )
    checkin_process_parser.add_argument(
        "--prefix",
        help="Add a prefix to generated links."
    )
    checkin_process_parser.add_argument(
        "--base_url",
        help="Base URL used to generate RSS channel and item links. Include a trailing /."
    )
    checkin_process_parser.set_defaults(func=handle_checkin_process)

    # Action: add
    checkin_add_parser = checkin_action_parser.add_parser("add")
    checkin_add_parser.add_argument(
        "--brewery",
        help="Name of the brewery."
    )
    checkin_add_parser.add_argument(
        "--beer",
        help="Name of the beer."
    )
    checkin_add_parser.add_argument(
        "--content_dir",
        help="Location of content to replace the default ./content/beer"
    )
    checkin_add_parser.set_defaults(func=handle_checkin_add)

    args = parser.parse_args()
    args.func(args)
