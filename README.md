# python_hw_19
Homework for 19 lesson

This script parses .log files and returns result both in console and dumps it in .json file, which is placed next \
to this script. 



Parsed info is:
1. Total amount of requests
2. Top 3 of requests IP addresses
3. Total amount of methods* of requests.
4. Top 3 requests with longest request time, with next stats:
   1. IP
   2. Method*
   3. referer URL

*NOTE: Everything that was stated as method in request gets parsed, even strings, that are obviously not valid HTTP methods