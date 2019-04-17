import requests
import json
import os
from constants import *
from getpass import getpass
from simplecrypt import encrypt, decrypt
from bs4 import BeautifulSoup


class BlackboardSession:
    def __init__(self, username=None, password=None):
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.loggedin = False
        self.updated = False

        cj = requests.utils.cookiejar_from_dict(
            {
                "allow_cookies": "true",
                "au_wayf_user": "true",
                "mitau_studerende_aktiv": "true",
            }
        )
        self.session.cookies = cj

    def set_username(self):
        self.username = input("Enter username: ")

    def set_password(self):
        exists = os.path.isfile(PASS_PATH)
        if not exists or not self.load_password():
            self.password = getpass("Enter password: ")
            self.update = True

    def save_password(self):
        file_password = getpass("Enter password for password file: ")
        exists = os.path.isfile(PASS_PATH)
        body = {}
        if exists:
            body = self.load_password_file(file_password=file_password)
        body[self.username] = self.password

        with open(PASS_PATH, "wb") as f:
            f.write(encrypt(file_password, json.dumps(body)))

    def load_password(self):
        body = self.load_password_file()
        if body[self.username]:
            self.password = body[self.username]
            return True
        return False

    def load_password_file(self, file_password=None):
        body = None
        with open(PASS_PATH, 'rb') as f:
            body = f.read()

        if file_password is None:
            file_password = getpass("Enter password for password file: ")
            
        dec = decrypt(file_password,body)
        return json.loads(dec)

    def get_auth(self):
        if self.username is None:
            self.set_username()

        if self.password is None:
            self.set_password()

        return {"username": self.username, "password": self.password}

    def login(self):
        print("Requesting bb website")
        resp = self.session.get("https://blackboard.au.dk")
        body = BeautifulSoup(resp.text, "html.parser")
        login_html = None
        for a in body.find_all("a"):
            if a.text == "Login":
                login_html = a.get("href")
                resp = self.session.get(login_html)
                break

        print(f"Logging in user {self.username}")
        resp = self.session.post(resp.url, data=self.get_auth())
        if "Forkert brugernavn eller kodeord" in resp.text:
            print("Forkert brugernavn eller kodeord")
            self.username = self.set_password = None
            self.login()

        if self.updated:
            print("Saving password")
            self.save_password()

        print("Following redirects")
        resp = self.follow_redirects(resp)
        self.loggedin = True

    def follow_redirects(self, response):
        body = BeautifulSoup(response.text, "html.parser")
        if body.find("form") is None:
            return response
        redirect_url = body.find("form").get("action")
        data = {}
        for input_elm in body.find_all("input"):
            data[input_elm.get("name")] = input_elm.get("value")

        if "SAMLResponse" not in data.keys():
            return response

        response = self.session.post(redirect_url, data=data)
        return self.follow_redirects(response)

    def get(self, url, **kwargs):
        if not self.loggedin:
            self.login()
        return self.session.get(url, **kwargs)


if __name__ == "__main__":
    bb = BlackboardSession()
    bb.login()
