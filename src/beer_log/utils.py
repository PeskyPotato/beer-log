import os
import markdown
from pathlib import Path


def clean_path(path):
    cwd = os.getcwd()

    path = Path(path)
    if path.is_absolute():
        return path.resolve()

    return os.path.join(cwd, path)


def parse_checkin_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(content)
        meta = md.Meta

        beer_score = -1
        if meta.get('beer_score') == '':
            beer_score = -1

        checkin_data = {
            'timestamp': meta.get('created_at', [None])[0],
            'rating_score': beer_score,
            'beer_name': meta.get('beer_name', [None])[0],
            'brewery_name': meta.get('brewery_name', [None])[0],
            'description': html,
            'image': meta.get('image', [None])[0]
        }
        return checkin_data
