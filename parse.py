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

for file in args.f:
    if file.endswith(".log"):
        with open(file) as log:
            logfile = log.read()

def total_requests():
    """
    :return: 1 for every valid request
    """
    re_request = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    list_of_ips = [x.group(0) for x in re.finditer(re_request, logfile, re.MULTILINE)]

    return list_of_ips


def top3_ips(list_of_ips):
    top_ips = {i: list_of_ips.count(i) for i in list_of_ips}
    sorted_ips = sorted(top_ips.items(), key=lambda ip: ip[1], reverse=True)
    return [{ip: count} for ip, count in sorted_ips[:3]]


def amount_of_http_methods():
    re_http_methods = r'(] ")((GET)|(POST)|(PUT)(PATCH)(UPDATE)(DELETE)(HEAD)(OPTIONS))'
    total_methods = [x.group(2) for x in re.finditer(re_http_methods, logfile, re.MULTILINE)]
    count_each_method = {i: total_methods.count(i) for i in total_methods}
    sorted_methods = sorted(count_each_method.items(), key=lambda x: x[1], reverse=True)
    return [{method: count} for method, count in sorted_methods]


def top3_logest_requests():
    logfilelist = logfile.splitlines()
    top3 = sorted(logfilelist, key=lambda request: request.split(" ")[-1], reverse=True)[:3]

    return top3


total_stats = {
    "Total Requests": len(total_requests()),
    "Top 3 IP adresses": top3_ips(total_requests()),
    "Total HTTP methods count": amount_of_http_methods(),
    "Top 3 longest requests": top3_logest_requests()
}
print(top3_logest_requests())
print(total_stats)