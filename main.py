#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description = "python script to parse telegram html chat logs exported by the desktop client") 
parser.add_argument("-i", "--input", nargs=1, required=True, type=argparse.FileType('r'))
parser.add_argument("-o", "--output", nargs=1, type=argparse.FileType('w'))
parser.add_argument("-f", "--format", nargs=1, choices=["text", "json", "plain"])
parser.add_argument("-v", "--verbose",  action='store_true')

parsed = parser.parse_args()



soup = BeautifulSoup(parsed.input[0], "html.parser")


alldefaultmesssages = soup.select(".message.default")


last_name = ""
for mess in alldefaultmesssages:
    textselection = mess.select_one(".text")
    # if textselection != None:
    #     print(textselection.text.strip())
    dateselection = mess.select_one(".date")
    # print(dateselection["title"])
    name = ""
    if "joined" in mess["class"]:
        name = last_name
    else:
        name = mess.select_one(".from_name").text.strip()
    print(name)

    if textselection != None:
        print(textselection.text.strip())

