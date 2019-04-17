# Blackboard-Scripts
The following is a collection of scripts for performing different actions on BlackBoard. BlackBoard is a learning platform used by Aarhus University. The class for interacting with blackboard is based on the following project: [bbfetch](https://github.com/Mortal/bbfetch)

## Dependencies
The dependencies for using this package is the following:
  - [Requests](http://docs.python-requests.org/en/master/) for sending request via HTTP
  - [simple-crypt](https://pypi.org/project/simple-crypt/) for encrypting the password file
  - [Beutiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for parsing HTML

## Using the BlackBoardSession class
The class `BlackBoardSession` takes to keyword arguments one for a `username` and one for a `password`. If they are not supplied it is going to ask for a username and password from the command line.

It automatically saves already know password in the file `.bbpass` file which is encrypted under some password chosen by the user the first time inputting a password. It is only saved when inputting through the terminal.

To request a page using an instance of this class the `get` function can be used.

## Downloading pdfs
To download a batch from blackboard the download.py file can be used as follows:
```bash
  ./download.py
```
Just follow the instructions on screen an input the desired URL and file extension
