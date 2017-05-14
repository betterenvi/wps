# -*- coding: utf-8 -*-
import os
import sys
import re
import codecs
from bs4 import BeautifulSoup


def read_file(filename):
    try:
        with codecs.open(filename, 'r', 'utf-8') as fin:
            print(filename)
            content = fin.read()
            return content
    except Exception as e:
        with open(filename, 'r') as fin:
            print(filename)
            content = fin.read()
            return content


def clean_html(html):
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    return text


def read_clean_html(filename):
    html = read_file(filename)
    text = clean_html(html)
    return text


def walkdir(rootdir, extension='.txt'):
    filelist = []
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith(extension):
                filelist.append(os.path.join(parent, filename))
    return filelist


def check_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

