from zipfile import ZipFile
import os
import argparse
import shutil
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from html.entities import name2codepoint
from zipfile import ZipFile
from math import ceil, log
import re
import string

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

data_xhtml = []

parser = argparse.ArgumentParser()
parser.add_argument("epubfile", help="put a path to your epub file in here")
args = parser.parse_args()
file_path = args.epubfile
file_name = os.path.basename(file_path)
epub_path = os.getcwd() +'/bionic_' + file_name
unzip_path_folder = file_name + '_zip/' 
unzip_path = os.getcwd() + '/' + unzip_path_folder


try:
    with ZipFile(file_path, 'r') as zipObj:
        zipObj.extractall(unzip_path)
except:
    with ZipFile(os.getcwd() + '/' + file_path, 'r') as zipObj:
        zipObj.extractall(unzip_path)

####################################
        

first_tags = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE xhtml PUBLIC '-//W3C//DTD XHTML 1.1//EN' 'http://www.w3.org/1999/xhtml'>\n"""


xhtmls = []
# r=root, d=directories, f = files
for r, d, f in os.walk(unzip_path):
    for hfile in f:
        if hfile[-4:] == 'xhtml':
            xhtmls.append(os.path.join(r, hfile))


for xhtml in xhtmls:
  
    with open(xhtml, 'r', encoding='utf-8') as f:
        html_data = f.read()

    data_xhtml = []
    parser = XHTMLParser()
    parser.feed(html_data)

    full_xhtml = ''
    for xhtml_part in data_xhtml:
        if xhtml_part[0] == 'Data:':
            full_xhtml += bolding(xhtml_part[1])
            

        if len(xhtml_part) == 2 and xhtml_part[0][0] == 'Start tag:':
            tag = '<' + xhtml_part[0][1] 
            full_attr = []
            for attr in xhtml_part[1][1]:
                full_attr.append(attr[0] + f'="{attr[1]}"')
            full_attr = ', '.join(full_attr)
            if not full_attr:
                tag += full_attr + '/>'
            else:
                tag += ' ' + full_attr + '/>'
            full_xhtml += tag
        if xhtml_part[0] == 'End tag:':
            tag = f"</{xhtml_part[1]}>"
            full_xhtml += tag
    full_xhtml = first_tags + full_xhtml

    with open(xhtml, 'w', encoding='utf-8') as f:
        f.write(full_xhtml)

####################################

os.chdir(unzip_path)
shutil.make_archive(epub_path, 'zip', './')
os.rename((epub_path + '.zip'), (epub_path + '.zip')[:-4])

