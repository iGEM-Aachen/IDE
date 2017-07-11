#!/usr/env python3
import glob
import re
import os

base_igem = 'http://2017.igem.org/'
base_team = base_igem + 'Team:Bristol/'
base_template = base_igem + 'Template:Bristol/'
base_raw = '?action=raw&ctype=text/'


def get_pages():
    pages = []
    for file in glob.glob('html/**/*.*', recursive=True):
        pages.append(file[5:])
    return pages


def build():
    links = create_links()
    for page in get_pages():
        with open('html/' + page, 'r') as f:
            text = f.read()
        for x in re.findall(r'\{\{([^}]+)\}\}', text):
            text = text.replace('{{' + x + '}}', links[x])
        write(page, text)


def create_links():
    links = {}
    for page in get_pages():
        if 'css/' in page:
            tmp = base_template + page[4:-4] + base_raw + 'css'
            links[page[:-4]] = '<link rel="stylesheet" type="text/css" href="' + tmp + '" />'
        elif 'js/' in page:
            tmp = base_template + page[3:-3] + base_raw + 'javascript'
            links[page[:-3]] = '<script type="text/javascript" src="' + tmp + '"></script>'
        elif 'templates/' in page:
            tmp = base_template + page[10:-5]
            links[page[:-5]] = '<link rel="import" href="' + tmp + '.html">'
        else:
            if 'index' in page:
                tmp = base_team + page[0:-10]
                links[page[:-5]] = tmp[:-1]
            else:
                links[page[:-5]] = base_team + page[0:-5]

    return links


def write(filename, output):
    filename = 'dist/' + filename
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(output)


if __name__ == '__main__':
    build()