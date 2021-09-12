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
            logfile = [x for x in log.readlines()]


def total_requests():
    list_of_ips = [('').join(ip.split(" ")[:1]) for ip in logfile]
    return list_of_ips


def top3_ips(list_of_ips):
    top_ips = {i: list_of_ips.count(i) for i in list_of_ips}
    sorted_ips = sorted(top_ips.items(), key=lambda ip: ip[1], reverse=True)
    return [{ip: count} for ip, count in sorted_ips[:3]]


def amount_of_http_methods():
    re_http_methods = r'(] ")((GET)|(POST)|(PUT)(PATCH)(UPDATE)(DELETE)(HEAD)(OPTIONS))'
    total_methods = [(re.search(re_http_methods, line, re.MULTILINE)).group(2) for line in logfile]
    count_each_method = {i: total_methods.count(i) for i in total_methods}
    sorted_methods = sorted(count_each_method.items(), key=lambda x: x[1], reverse=True)
    return [{method: count} for method, count in sorted_methods]


def top3_longest_requests():
    top3 = sorted(logfile, key=lambda request: request.split(" ")[-1], reverse=True)[:3]
    return top3


print(len(total_requests()))
print(top3_ips(total_requests()))
print(amount_of_http_methods())
print(top3_longest_requests())