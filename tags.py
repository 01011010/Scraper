
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup as soup
import requests
import argparse
import os
import sys
import jsbeautifier
# urlopen requires ssl certs
# go to the python folder and run
# /Applications/Python 3.10/Install Certificates.command

# HELP
parser = argparse.ArgumentParser(
    description='Get <script> tags from website or bautify single js file.')

# action: the basic type of action to be taken
parser.add_argument('-u', '--url', help='Target url')
parser.add_argument('-s', '--src', action='store_true',
                    help='Get only script tags with src')
parser.add_argument('-a', '--all', action='store_true',
                    help='Get all <script> tags')
parser.add_argument('-g', '--get', action='store_true',
                    help='Get target file from (--url)')
parser.add_argument('-b', '--beauty', action='store_true',
                    help='Beautify the file (redirect with > newfile)')
args = parser.parse_args()

# Target url
url = urlopen(args.url)
# Parse the site
soup = soup(url.read(), features="html.parser")

# Download a single file and beautify it
# note: redirect stdout to a new file -b > new_beauty.js
if args.get:
    filename = os.path.basename(urlparse(args.url).path)
    response = requests.get(args.url)
    open(filename, "wb").write(response.content)

    if args.beauty:
        res = jsbeautifier.beautify_file(filename)
        print(res)
    sys.exit()

# This gets both <script> and <script src>
if args.all:
    for link in soup.find_all('script'):
        print(link)
else:
    for link in soup.find_all('script', src=args.src):
        if args.src:
            print(link.get('src'))
        else:
            print(link)
