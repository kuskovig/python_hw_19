#!/usr/bin/env python3

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

# initializing all needed variables to store parsed data

dict_of_ips = {}
top3_ips = []
re_http_methods = r'(] ")((GET)|(POST)|(PUT)(PATCH)(UPDATE)(DELETE)(HEAD)(OPTIONS))'
dict_of_methods = {}
top3_request_by_duration = {}

"""
Method stores unique IP addresses and counts times they appear
"""


def parse_ips(value):
    if value in dict_of_ips.keys():
        dict_of_ips[value] += 1
    else:
        dict_of_ips[value] = 1


"""
Method stores unique HTTP methods  and counts times they appear
"""


def parse_methods(value):
    if value in dict_of_methods.keys():
        dict_of_methods[value] += 1
    else:
        dict_of_methods[value] = 1


"""
For every .log file in folder:
1. Opens file, reads line by line by line
2. Gathers IP, method, referer URL and duration of request
3. After reading file - combines all info and processes it. Result is printed in console and dumped in .json file
4. Before reading next file - clears variables which store parsed info

"""

for file in args.f:
    if file.endswith(".log"):
        # resetting variables
        dict_of_ips.clear()
        top3_ips.clear()
        dict_of_methods.clear()
        with open(file) as log:
            for line in log:
                # gathering IP address
                ip = ''.join(line.split(" ")[:1])
                parse_ips(ip)

                # gathering method with Regexp
                method = (re.search(re_http_methods, line, re.MULTILINE)).group(2)
                parse_methods(method)

                # gathering duration and referer url
                duration = int(line.strip().split(" ")[-1])
                url = line.split('\"')[-4]

                # Only saving info about top3 request  by longest duration
                if len(top3_request_by_duration) < 3:
                    top3_request_by_duration[duration] = "IP = " + ip + ", Method = " + method + ", URL= " + url
                else:
                    least_duration = min(top3_request_by_duration.keys())
                    if duration > least_duration:
                        top3_request_by_duration.pop(least_duration)
                        top3_request_by_duration[duration] = "IP = " + ip + ", Method = " + method + ", URL= " + url

            top3_ips = sorted(dict_of_ips.items(), key=lambda x: x[1], reverse=True)[:3]
            methods = sorted(dict_of_methods.items(), key=lambda x: x[1], reverse=True)
            top3_requests_sorted = sorted(top3_request_by_duration.items(), key=lambda x: x[0], reverse=True)

            result = {
                "Total Requests": sum(dict_of_ips.values()),
                "Top 3 IPs and their count": [{key: value} for key, value in top3_ips],
                "Methods and their count": [{key: value} for key, value in methods],
                "Top 3 by duration and related IP + Method + URL": [{key: value} for key, value in top3_requests_sorted]
            }

            print(f"===================Parsing result for {file}:")
            for item in result.items():
                print(item)
            with open(f"result for {file}.json", "w") as writer:
                json.dump(result, writer, indent=4)
