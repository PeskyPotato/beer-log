import argparse
import os
from datetime import datetime
from .main import BeerLog


def handle_process_checkins(args):
    kwargs = {}
    if args.templates_dir is not None:
        kwargs['templates_dir'] = args.templates_dir
    if args.content_dir is not None:
        kwargs['content_dir'] = args.content_dir
    if args.output_dir is not None:
        kwargs['output_dir'] = args.output_dir

    bl = BeerLog(**kwargs)
    bl.process_checkins()


def handle_checkin(args):
    content__dir = os.path.join("./", "content", "beer")
    if args.content_dir:
        content__dir = args.content_dir

    if args.timestamp:
        timestamp = datetime.fromisoformat(args.timestamp)
    else:
        timestamp = datetime.now()

    filename = f"{timestamp.strftime('%Y-%m-%d-%H')}-{args.brewery.lower()}-{args.beer.lower()}.md"
    filepath = os.path.join(content__dir, filename)
    with open(filepath, "w") as f:
        f.write(f"""---
beer_name: {args.beer}
beer_style:
brewery_name: {args.brewery}
created_at: {str(timestamp)}
beer_score:
serving_style:
image:
---

""")
    # TODO: Open file after creating boilerplate.
    

def entry():
    # TODO: Redo argument syntax to have namespaces by entity then action.
    # Create namespaces by entity, followed by actions, then required
    # or optionals arguments. For example `beer-log checkin process` or
    # `beer-log brewery add --name "Oproer"`.

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
    process_checkins_parser.add_argument(
        "--output_dir",
        help="Location of rendered HTML files to replace the default ./beer"
    )
    process_checkins_parser.set_defaults(func=handle_process_checkins)

    checkin_parser = subparser.add_parser("checkin")
    checkin_parser.add_argument(
        "brewery",
        help="Name of the brewery that made the beer."
    )
    checkin_parser.add_argument(
        "beer",
        help="Name of the beer."
    )
    checkin_parser.add_argument(
        "--content_dir",
        help="Location of content to replace the default ./content/beer"
    )
    checkin_parser.add_argument(
        "--timestamp",
        help=""
    )
    checkin_parser.set_defaults(func=handle_checkin)

    args = parser.parse_args()
    args.func(args)
