import string
import re
from math import ceil, log
from bs4 import BeautifulSoup, Tag 

def bolding(text):
    pattern = r"\b\w+'?\w*\b"
    parts = re.findall( pattern, text)
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

def bold_specific_text(tag):
    # Apply bolding to the entire text content of the tag
    new_content = bolding(tag.text)
    
    # Clear the existing content of the tag
    tag.clear()

    # Parse the modified content as HTML and append it to the tag
    tag.append(BeautifulSoup(new_content, 'html.parser'))


def unbold_specific_text(soup, tag):
    new_tag = Tag(soup, name='div')
    new_tag.attrs = tag.attrs
    # new_tag.contents = tag.contents
    new_tag.contents = bolding(tag.text)
    tag.replace_with(new_tag)
    return tag
