#!/usr/bin/env python3
"""Parses Telegram """
import argparse
from datetime import datetime
import json
from bs4 import BeautifulSoup


class TelegramMessage:
    """Class wrapping a telegram message"""
    def __init__(self, date: datetime, sender: str, message: str):
        self.date = date
        self.sender = sender
        self.message = message

    def to_text_string(self):
        """ returns Message as a full Text String"""
        return "["+self.date.isoformat()+"] "+self.sender +": "+self.message

    def to_object(self):
        """ Do fucking shit"""
        return {"date": self.date.isoformat(),
                "sender": self.sender,
                "message": self.message}

    def to_plain_string(self):
        """ returns just the message """
        return self.sender +": "+ self.message

    def to_html(self):
        """ return in html format"""
        return "<b>"+self.sender +"</b>: "+ self.message

def main():
    """ main function of script """
    parser = argparse.ArgumentParser(description=
                                     """python script to parse telegram
                                     html chat logs exported by the desktop client""")
    parser.add_argument("-i", "--input", nargs=1, required=True, type=argparse.FileType('r'))
    parser.add_argument("-o", "--output", nargs=1, type=argparse.FileType('a'))
    parser.add_argument("-f", "--format", nargs=1, choices=["text", "json", "plain", "html"])
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("-r", "--replace", nargs="*")

    parsed = parser.parse_args()
    print(parsed)

    if parsed.replace is not None:
        if len(parsed.replace)%2 != 0:
            print("If you are using the replace tool, please use an even number, you fucking brick")
            return

    soup = BeautifulSoup(parsed.input[0], "html.parser")


    alldefaultmesssages = soup.select(".message.default")

    objects = []
    last_name = ""
    for mess in alldefaultmesssages:
        textselection = mess.select_one(".text")
        dateselection = mess.select_one(".date")
        date = datetime.strptime(dateselection["title"], "%d.%m.%Y %H:%M:%S")

        name = ""
        if "joined" in mess["class"]:
            name = last_name
        else:
            name = mess.select_one(".from_name").text.strip()
            last_name = name

        if parsed.replace is not None:
            if name in parsed.replace[::2]:
                name = parsed.replace[parsed.replace.index(name)+1]
                last_name = name


        if textselection is not None:
            obj = TelegramMessage(date, name, textselection.text.strip())
            objects.append(obj)
            if parsed.verbose is True:
                print(obj.to_text_string())
    
    if parsed.format[0] == "json":
        json.dump([x.to_object() for x in objects], parsed.output[0])
    elif parsed.format[0] == "text":
        for exs in objects:
            parsed.output[0].write(exs.to_text_string()+"\n")
    elif parsed.format[0] == "plain":
        for exs in objects:
            parsed.output[0].write(exs.to_plain_string()+"\n")
    elif parsed.format[0] == "html":
        for exs in objects:
            parsed.output[0].write(exs.to_html()+"\n")



if __name__ == "__main__":
    main()
