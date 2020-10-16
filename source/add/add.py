from os import path as pathlib,popen
from argparse import ArgumentParser
from requests import post
from requests.exceptions import ConnectionError
from json import loads

from sys import exit


parser = ArgumentParser()
parser.add_argument("file",help="File Path Or Name",type=str)
parser.add_argument("-t","--type",help="1 for open sharing 0 for private sharing",type=int,default=1)
parser.add_argument("--force",help="setting it true will update existing token",type=bool,default=False)
parser.add_argument("--local",help="set this true when sharing file locally",type=bool,default=False)

"""
App Config

linux/unix : ✔️
windows    : ⭕
mac        : ⭕
"""

_USERNAME,_ = popen("whoami").read().split("\n") 
_PATH       = pathlib.join("/home/",_USERNAME,".transferpi")
_REQUEST = dict(
    file=None,
    type=None,
    local=False
)

try:_CONFIG = loads(open(pathlib.join(_PATH,"config.json"),"r").read())
except:exit(print("Config File Not Fouund !"))

def main(args):
    file = pathlib.abspath(args.file)
    if not pathlib.isfile(file):
        print("File Does Not Exist ¯\\_(ツ)_/¯")
        exit(0)

    _REQUEST['file'] = file
    _REQUEST['type'] = args.type
    
    try:
        response = post(
                "http://localhost:2121/file/new",
                json=_REQUEST,
                headers={
                    "Authentication":_CONFIG['account_keys']['private']
                }
            )        
    except ConnectionError:
        exit(print ("Error, Fileserver Not Running"))

    if response.status_code == 200:
        response = loads(response.text)
        for i in response:
            print (f"[+] {i}{' '*(16-len(i))}: {response[i]}")
    else:
        print (response.json()['message'])

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)