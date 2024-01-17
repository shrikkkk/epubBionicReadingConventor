from zipfile import ZipFile
import os
import argparse
import shutil
from xhtmlParser import XHTMLParser, bolding


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
