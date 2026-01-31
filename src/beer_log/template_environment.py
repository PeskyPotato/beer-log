from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class TemplateEnvironment:
    _root = os.path.dirname(os.path.abspath(__file__))
    def __init__(self, templates_dir=os.path.join(_root, 'templates')):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.env.lstrip_blocks = True
        self.env.trim_blocks = True
        self.env.filters["from_timestamp"] = self.from_timestamp
        self.env.filters["date"] = self.date_format

        self.status = True

    def from_timestamp(self, timestamp, fmt="iso"):
        published_dt = datetime.fromtimestamp(timestamp)
        if fmt == "human":
            return published_dt.strftime("%d.%m.%Y")

        return published_dt.strftime("%Y-%m-%dT%H:%M:%S.%f%z")


    def date_format(self, value, fmt="%Y-%m-%d"):
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return dt.strftime(fmt)

