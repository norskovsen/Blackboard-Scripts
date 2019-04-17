#!/usr/bin/python3

from blackboard import BlackboardSession
from constants import *
from bs4 import BeautifulSoup
import re


def download_and_find_pdfs(url, extension):
    bb = BlackboardSession()
    names, urls = locate_pdfs(re.compile(f".*{extension}"), bb, url)
    download_pdfs(bb, names, urls)


def locate_pdfs(regex, bb, url):
    resp = bb.get(url)
    body = BeautifulSoup(resp.text, "html.parser")
    print("Finding urls")
    names = []
    urls = []
    for a_elm in body.find_all("a"):
        if len(regex.findall(a_elm.text)) > 0:
            print(f"Found: {a_elm.text}")
            names.append(a_elm.text.strip())
            url = a_elm.get("href")
            if url[0] == '/':
                url = MAIN_URL + url
            print(url)
            urls.append(url)
    return names, urls


def download_pdfs(bb, names, urls):
    for name, url in zip(names, urls):
        print(f"Downloading {name}")
        resp = bb.get(url)
        with open(name, "wb") as f:
            f.write(resp.content)


if __name__ == "__main__":
    download_and_find_pdfs(input("Enter url: "), input("Enter file extension: "))
