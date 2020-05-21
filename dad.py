#
# This application manipulates the godaddy API
#
# 20200519 - Al Biheiri <al@forgottheaddress.com>

import requests
import argparse
import sys


# Read the config file
try:
    text_file = open("cred.conf", "r")
    lines = text_file.read().split(',')
    # print (lines[0])
    # print (lines[1])
    text_file.close()
except:
    print ("File: cred.conf not found.")
    exit(1)


def get(domain, record_type, value):
    #auth = 'USER:PASSW'
    auth = f"{lines[0]}:{lines[1]}".rstrip()
    # print (auth)
    headers = {'accept': 'application/json', 'Authorization':  f"sso-key {auth}"}
    
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{value}'
    r = requests.get(url, headers=headers)

    #print(r.url)
    print(r.text)
    # print(r.request.headers)

#
# Parse the arguments
#

# TODO: Format the help - https://stackoverflow.com/questions/50021282/python-argparse-how-can-i-add-text-to-the-default-help-message/50021346
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("record", choices=['A', 'TXT', 'AAAA'], help="the record type")
parser.add_argument("value", help="the name of the record")
group.add_argument("-g", "--get", help="get from domain")
group.add_argument("-a", "--add", help="add to domain")
group.add_argument("-d", "--del", help="delete from domain")
args = parser.parse_args()

if args.get:
    get(args.get, args.record, args.value)
else:
    print ("Not implemented yet")

