import argparse
from .main import process_checkins

def entry():
    parser = argparse.ArgumentParser()
    parser.add_argument("process_checkins")
    args = parser.parse_args()
    if args.process_checkins:
        print("process checkins")
