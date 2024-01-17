
import argparse
import os
import shutil
from zipfile import ZipFile
from modifier import bold_specific_text
from bs4 import BeautifulSoup

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


xhtmls = []
# r=root, d=directories, f = files
for r, d, f in os.walk(unzip_path):
    for hfile in f:
        if hfile[-5:] == 'xhtml':
            xhtmls.append(os.path.join(r, hfile))


for xhtml in xhtmls:
  
    with open(xhtml, 'r', encoding='utf-8') as f:
        html_data = f.read()
        soup = BeautifulSoup(html_data, 'html.parser') 

        all_paragraphs = soup.find_all('p')
        for paragraph in all_paragraphs:
            bold_specific_text(paragraph)


    with open(xhtml, 'w', encoding='utf-8') as file:
        file.write(str(soup))

os.chdir(unzip_path)
shutil.make_archive(epub_path, 'zip', './')
os.rename((epub_path + '.zip'), (epub_path + '.zip')[:-4])

