#
# This application manipulates the godaddy API
#
# 20200519 - Al Biheiri <al@forgottheaddress.com>

prog='dad'
version='0.1'
author='Al Biheiri (al@forgottheaddress.com)'

import requests, argparse, sys


# Read the config file
try:
    text_file = open("cred.conf", "r")
    lines = text_file.read().split(',')
    # print (lines[0])
    # print (lines[1])
    text_file.close()
except:
    print ("File: cred.conf not found or malformed data.")
    exit(1)


# Constructs your HTTP headers
def headers():
    # Array from reading the file, removing newline
    auth = f"{lines[0]}:{lines[1]}".rstrip()
    
    # Let other functions see this
    global headers
    headers = {'accept': 'application/json', 'Authorization':  f"sso-key {auth}"}


# TODO: implement this
# Checks for avail for sale domains
def do_search(domain):
    headers ()
    payload = {'domain': 'name'}
    url = f'https://api.godaddy.com/v1/domains/available?{payload}&checkType=FAST&forTransfer=false'
    r = requests.get(url, headers=headers)
    print(r.text)



# Check avail domain
# "https://godaddy.com/v1/domains/available?domain=boboyaz1.co&checkType=FAST&forTransfer=false"

# Gets records from your domain
def do_get(domain, record_type, name):
    headers ()
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{name}'    
    r = requests.get(url, headers=headers)
    print(r.text)

    #print(r.url)
    # print(r.request.headers)

def do_add(domain, record_type, name, value, ttl):
     #curl -X PATCH https://api.godaddy.com/v1/domains/biheiri.com/records
     #-H 'Authorization: sso-key KEY:VAL'
     #-H 'Content-Type: application/json'
     # --data '[{"type": "A","name": "blnk1","data": "192.1.2.2,"ttl": 3600"}]’
    headers ()
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/'    
    r = requests.patch(url, headers=headers, data = {'type': f'{record_type}', 'name': f'{name}', 'data': f'{value}', 'ttl': f'{ttl}'})
    print(r.text)
    print ('type',record_type, 'name', name, 'data', value, 'ttl', ttl)
    


#
# Parse the arguments
#

# TODO: Format the help - https://stackoverflow.com/questions/50021282/python-argparse-how-can-i-add-text-to-the-default-help-message/50021346
parser = argparse.ArgumentParser( 
usage=\
'''dad.py [-h] [-g GET | -a ADD | -d DELETE] -r {A,AAAA,CNAME,TXT,MX,SRV,SOA,NS} -n NAME [-v VALUE] [--ttl TTL]

Get a record:
dad.py -g abiheiri.com -r A -n www

Add a record:
dad.py -a abiheiri.com -r A -n wwww -v 192.168.0.1 -t 3600

Delete a record:
(not implemented)
''', 

#description='',

 epilog= \
'''GoDaddy customers can obtain values for the KEY and SECRET arguments by creating a production key at
https://developer.godaddy.com/keys/.''')

group = parser.add_mutually_exclusive_group()
parser.add_argument('--version', action='version', version='{} {}'.format(prog, version))
group.add_argument("-g", dest="get", metavar='mydomain.com', help="get from this domain")
group.add_argument("-a", dest="add", metavar="mydomain.com", help="add from this domain")
group.add_argument("-d", dest="delete", metavar="mydomain.com", help="delete from this domain")
parser.add_argument("-r", dest="record", required=True, choices=['A','AAAA','CNAME','TXT','MX','SRV','SOA','NS'], help="choose record type")
parser.add_argument("-n", dest="name", required=True, metavar="myhostname", help="the dns record name")
parser.add_argument("-v", dest="value", metavar="192.168.0.1", help="the value of the dns record")
parser.add_argument('--ttl', type=int, default=3600, help='default is 3600')
#group.add_argument("-s", "--search", help="search domain for sale")
args = parser.parse_args()

if args.get:
    print(args.name)
    do_get(args.get, args.record, args.name)
if args.add:
    print(args.name)
    do_add(args.add, args.record, args.name, args.value, args.ttl)


