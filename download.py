#!/usr/bin/python3

from blackboard import BlackboardSession
from constants import *
from bs4 import BeautifulSoup
import re
import argparse


def download_and_find_pdfs(result):
    url, extension = result.url, result.extension
    if url is None:
        url = input("Enter url: ")
    
    if extension is None:
        extension = input("Enter extension: ")

    bb = BlackboardSession(username=result.username, password=result.password)
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
            urls.append(url)
    return names, urls


def download_pdfs(bb, names, urls):
    for name, url in zip(names, urls):
        print(f"Downloading {name}")
        resp = bb.get(url)
        with open(name, "wb") as f:
            f.write(resp.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download files from Blackboard")
    parser.add_argument('-u', '--user', action='store', dest='username', help = "username for blackboard")
    parser.add_argument('-p', '--password', action='store', dest='password', help = "password for blackboard")
    parser.add_argument('-l', '--url' , action='store', dest='url', help="url for blackboard site with links")
    parser.add_argument('-e', '--extension', action='store', dest='extension', help = "file extension of the given files")
    parser.add_argument('-v', '--version',action='version',
                        version='Blackboard Downloader version 0.1')
    result = parser.parse_args()

    try:
        download_and_find_pdfs(result)
    except KeyboardInterrupt:
        pass
