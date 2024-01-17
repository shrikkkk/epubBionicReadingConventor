import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from html.entities import name2codepoint
from zipfile import ZipFile
from math import ceil, log
import re
import string
import os



class XHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data_xhtml = []

    def handle_starttag(self, tag, attrs):
        global data_xhtml
        attributes = []
        for attr in attrs:
            attributes.append(attr)
        data_xhtml.append((("Start tag:", tag), ("attr:", attributes)))


    def handle_endtag(self, tag):
        global data_xhtml
        data_xhtml.append(("End tag:", tag))

    def handle_data(self, data):
        global data_xhtml
        data_xhtml.append(("Data:", data))

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))

    def handle_decl(self, data):
        pass

def bolding(text):
    parts = re.findall( r'\w+|[^\s\w]+', text)
    new_text = ''
    for part in parts:
        if part in string.punctuation or part in string.digits:
            new_text += part
        else:
            if len(part) <= 3:
                new_part = ''
                new_part = f"<b>{part[0]}</b>"
                new_part += ''.join(part[1:])
                new_text += ' ' + new_part
            else:
                point = ceil(log(len(part), 2))
                new_part = ''
                new_part = f"<b>{part[0:point]}</b>"
                new_part += ''.join(part[point:])
                new_text += ' ' + new_part 
    return new_text   