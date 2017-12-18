#!/usr/bin/env python
import os
import argparse
import sys
import html

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import json
from pprint import pprint

import time
from calendar import timegm
from datetime import datetime, date

from jinja2 import Environment, PackageLoader, select_autoescape

#
# MIT License
#
# https://opensource.org/licenses/MIT
#
# Copyright 2017 Rene Sugar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def str_to_datetime(datetime_str):
    if datetime_str.isdigit() == True:
        dt = date(year=int(datetime_str),day=1,month=1)
    else:
        # Date/time can be in several different formats
        try:
            dt = datetime.strptime(datetime_str, '%b %d %Y %H:%M:%S %Z')
        except ValueError:
            try:
                dt = datetime.strptime(datetime_str, '%a %b %d %Y %H:%M:%S %Z%z')
            except ValueError:
                dt = datetime.strptime(datetime_str, '%b %d %Y %H:%M:%S %Z%z')

    return dt

def main():
    parser = argparse.ArgumentParser(description="timeline")
    parser.add_argument("--path", help="Path of the XML file to be scanned")
    parser.add_argument("--template", help="Path of the template file")
    parser.add_argument("--title", help="Title of the timeline")
    args = vars(parser.parse_args())

    xmlPath = os.path.abspath(os.path.expanduser(args['path']))

    templatePath = args['template']

    templateTitle = args['title']

    tree = ET.ElementTree(file=xmlPath)

    root = tree.getroot()

    env = Environment(
        loader=PackageLoader('timeline', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    event_id = 0

    events = []

    for child in root:
        title = ""
        start_date = ""
        end_date = ""
        description = html.unescape(child.text)

        event = {}

        for name, value in child.attrib.items():
            if name == "title":
                title = value
            elif name == "start":
                start_date = str_to_datetime(value).strftime("%Y-%m-%d")
            elif name == "end":
                end_date = str_to_datetime(value).strftime("%Y-%m-%d")

        event_id += 1

        event["id"] = "Event {event_id}".format(event_id=event_id)
        event["name"] = title
        event["start"] = start_date
        event["end"] = end_date
        event["progress"] = 0
        event["dependencies"] = ""
        event["description"] = description

        events.append(event)
  
    template = env.get_template(templatePath)

    print(template.render(title=templateTitle, items=events))

if __name__ == "__main__":
  main()