import re
import argparse
import os
import json


def check_path(path):
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        return os.listdir(path)
    else:
        raise argparse.ArgumentTypeError("Pass a valid path to .log file or to the directory ")


parser = argparse.ArgumentParser(description="Parses the log file")
parser.add_argument("--f",
                    help="Pass a valid path to the .log file or to the directory",
                    type=check_path)
args = parser.parse_args()

re_request = r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"

for file in args.f:
    if file.endswith(".log"):
        with open(file) as log:
            dict = [
                {"total_requests": len([1 for x in re.finditer(re_request, log.read(), re.MULTILINE)])},

                    ]
            print(dict)

# if os.path.isfile(args.f):
#     with open(args.f) as file:
#         print(file.read())
#
# if os.path.isdir(args.f):
#     for file in os.listdir():
#         if file.endswith(".log"):
#             with open(file) as log:
#                 print(log.read())
