import os
import markdown
from pathlib import Path
from datetime import datetime, timezone


def clean_path(path):
    cwd = os.getcwd()

    path = Path(path)
    if path.is_absolute():
        return path.resolve()

    return os.path.join(cwd, path)


def parse_checkin_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        md = markdown.Markdown(extensions=["meta"])
        html = md.convert(content)
        meta = md.Meta

        # TODO: Can we simplify the arrays here?
        beer_score = meta.get("beer_score", -1)
        if meta.get("beer_score") == "":
            beer_score = [-1]
        checkin_data = {
            "timestamp": meta.get("created_at", [None])[0],
            "rating_score": beer_score[0],
            "beer_name": meta.get("beer_name", [None])[0],
            "brewery_name": meta.get("brewery_name", [None])[0],
            "description": html,
            "image": meta.get("image", [None])[0],
        }
        return checkin_data


def to_datetime(value):
    try:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f %z")
    except ValueError:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def clean_filenames(value):
    # Used to escape some characters in filenames
    # Converts string to lowercase, replaces spaces with
    # a hyphen.
    return value.lower().replace(" ", "-")
