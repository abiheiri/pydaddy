#
# This application manipulates the godaddy API
#
# 20200519 - Al Biheiri <al@forgottheaddress.com>

prog='dad'
version='0.1'
author='Al Biheiri (al@forgottheaddress.com)'

import requests, argparse, sys


def OpenAuthFile():
    try:
        text_file = open("cred.conf", "r")
        global lines
        lines = text_file.read().split(',')
        global api_key
        global secret_key
        api_key = lines[0]
        secret_key = lines[1]
        text_file.close()
    except:
        print ("File: cred.conf not found or malformed data.")
        exit(1)


    


# TODO: implement search avail for sale domains
# "https://godaddy.com/v1/domains/available?domain=boboyaz1.co&checkType=FAST&forTransfer=false"

# TODO: implement delete
#
# get all domain records https://api.godaddy.com/v1/domains/biheiri.com/records/
# iterate, collect, subtract, repopulate
# load data to do_add function

# Gets records from your domain
def do_get(domain, record_type, name):
    headers = {'Accept': 'application/json', 'Authorization':  "sso-key {}:{}".format(api_key, secret_key)}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}/{name}'    
    r = requests.get(url, headers=headers)
    print(r.text)


def do_add(domain, record_type, name, value, ttl):
    headers = {'Content-Type': 'application/json', 'Authorization':  "sso-key {}:{}".format(api_key, secret_key)}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records'

    payload = ("[{\"type\": \"%s\",\"name\": \"%s\",\"data\": \"%s\",\"ttl\": %s}]" % (record_type, name, value, ttl))

    # r = requests.request("PATCH", url, headers=headers, data = payload)
    # print(r.text.encode('utf8'))
    # print(domain)

    r = requests.patch(url, headers=headers, data=payload)
    print(r.text)

    if r.status_code == 200:
        print('Success!')
    else:
        print('Whoopsie... HTTP Error:', r.status_code)

#
# Parse the arguments
#


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
parser.add_argument("-r", dest="record", choices=['A','AAAA','CNAME','TXT','MX','SRV','SOA','NS'], help="choose record type")
parser.add_argument("-n", dest="name", metavar="myhostname", help="the dns record name")
parser.add_argument("-v", dest="value", metavar="192.168.0.1", help="the value of the dns record")
parser.add_argument('--ttl', type=int, default=3600, help='default is 3600')
#group.add_argument("-s", "--search", help="search domain for sale")
args = parser.parse_args()

if args.get:
    OpenAuthFile()
    do_get(args.get, args.record, args.name)
if args.add:
    OpenAuthFile()
    do_add(args.add, args.record, args.name, args.value, args.ttl)
else:
    print("You dont know what you are doing. Try using the -h flag")


