#!/usr/bin/env python
#
# This application manipulates the godaddy API
#
# 20200519 - Al Biheiri <al@forgottheaddress.com>



import requests, argparse, sys

prog='dad'
version='0.5'
author='Al Biheiri (al@forgottheaddress.com)'

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
        print ('''File: cred.conf not found or malformed data. Make sure the file only has KEY,SECRET
        GoDaddy customers can obtain values for the KEY and SECRET arguments by creating a production key at https://developer.godaddy.com/keys/.
        ''')
        exit(1)



 #
 # Troubleshooting
 # 
 # print (r.content)   



# TODO: implement delete
#
# get all domain records https://api.godaddy.com/v1/domains/biheiri.com/records/
# iterate, collect, subtract, repopulate
# load data to do_add function

# Checking a domain avail for sale
def do_sale(domain):
    headers = {'Accept': 'application/json', 'Authorization':  "sso-key {}:{}".format(api_key, secret_key)}
    url = f'https://api.godaddy.com/v1/domains/available?domain={domain}'    
    r = requests.get(url, headers=headers)
    print(r.text)

def do_get(domain, record_type):
    headers = {'Accept': 'application/json', 'Authorization':  "sso-key {}:{}".format(api_key, secret_key)}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/{record_type}'    
    r = requests.get(url, headers=headers)
    print(r.text)


def do_replace(domain, record_type, name, value, ttl):
    headers = {'Content-Type': 'application/json', 'Authorization':  "sso-key {}:{}".format(api_key, secret_key)}
    url = f'https://api.godaddy.com/v1/domains/biheiri.com/records/A/blnk1'

    payload = ("[{\"type\": \"%s\",\"name\": \"%s\",\"data\": \"%s\",\"ttl\": %s}]" % (record_type, name, value, ttl))
    
    r = requests.put(url, headers=headers, data = payload)
    print(r.text)

    if r.status_code == 200:
        print('Success!')

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
        if 'DUPLICATE_RECORD' in r.text:    
            print ("Try using the -r (replace) option")
        

#
# Parse the arguments
#

def goto_help ():
    print ("help!")
    exit()

# g,a,d,s - can not be combined
# -g(domain)->r(record_type)
# -a(domain)->r(record_type),n(name),v(value) ?ttl
# -d(domain)->r(record_type),n(name)
# -s(domain)

parser = argparse.ArgumentParser(
usage=\
'''dad.py [-h HELP] [-g GET|-a ADD|-r REPLACE|-s SEARCH] -rt {A,AAAA,CNAME,TXT,MX,SRV,SOA,NS} -n NAME [-v VALUE] [--ttl TTL]

=======================================================
This tool leverages the GoDaddy domains API 
so you can make DNS changes without using their website.
=======================================================

Get all 'A' records from a domain
dad.py -g abiheiri.com -rt A

Get all 'TXT' records from a domain
dad.py -g abiheiri.com -rt TXT

Add a new record:
dad.py -a abiheiri.com -rt A -n www -v 192.168.0.1 -t 3600
dad.py -a abiheiri.com -rt MX -n smtphost01 -v 192.168.0.1

Replace an existing record:
dad.py -r abiheiri.com -rt A -n wwww -v 192.168.0.1 -t 3600
dad.py -r abiheiri.com -rt A -n wwww -v 192.168.0.1

Delete a record:
(not implemented yet)
''',

#description='',

epilog= \
'''GoDaddy customers can obtain values for the KEY and SECRET arguments by creating a production key at
https://developer.godaddy.com/keys/.''')



parser.add_argument('--version', action='version', version='{} {}'.format(prog, version))

group = parser.add_mutually_exclusive_group()
group.add_argument("-g", dest="get", metavar='get', help="get all records from a domain")
group.add_argument("-a", dest="add", metavar="add", help="add to domain")
group.add_argument("-r", dest="replace", metavar="replace", help="replce record in a domain")
group.add_argument("-d", dest="delete", metavar="delete", help="delete record a domain")
group.add_argument("-s", dest="search", metavar="search", help="search domain for sale")

parser.add_argument("-rt", dest="record", metavar="record type", choices=['A','AAAA','CNAME','TXT','MX','SRV','SOA','NS'], help="A,AAAA,CNAME,TXT,MX,SRV,SOA,NS")
parser.add_argument("-n", dest="name", metavar="name", help="the dns record name")
parser.add_argument("-v", dest="value", metavar="value", help="the value of the dns record (ie. ip address)")
parser.add_argument('--ttl', type=int, default=3600, help='default is 3600 if this argument is not supplied')

args = parser.parse_args()

if args.get:
    OpenAuthFile()
    do_get(args.get, args.record)

elif args.add:
    OpenAuthFile()
    
    #Checking that you passed min req
    if len(sys.argv) >= 9:
        do_add(args.add, args.record, args.name, args.value, args.ttl)
    else:
        print("Arguments missing")

elif args.replace:
    OpenAuthFile()

    #Checking that you passed min req
    if len(sys.argv) >= 9:
        do_replace(args.replace, args.record, args.name, args.value, args.ttl)
    else:
        print("Arguments missing")
    
elif args.search:
    OpenAuthFile()
    do_sale(args.search)    

elif args.delete:
    print("not implemented yet") 

else:
    print("You dont know what you are doing. Try using the -h flag")


