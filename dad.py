#
# This application manipulates the godaddy API
#
# 20200519 - Al Biheiri <al@forgottheaddress.com>


import requests

#curl -X GET "https://api.godaddy.com/v1/domains/abiheiri.com/records/A/%40" -H "accept: application/json" -H "Authorization: sso-key KEYVAL:SECRETPASS"

#payload = {'key1': 'value1', 'key2': 'value2'}
#r = requests.get('https://httpbin.org/get', params=auth)


# Read the config file

text_file = open("cred.conf", "r")
lines = text_file.read().split(',')
# print (lines[0])
# print (lines[1])
text_file.close()


#auth = 'USER:PASSW'
auth = f"{lines[0]}:{lines[1]}".rstrip()
# print (auth)
headers = {'accept': 'application/json', 'Authorization':  f"sso-key {auth}"}


url = 'https://api.godaddy.com/v1/domains/abiheiri.com/records/A/@'
r = requests.get(url, headers=headers)

# print(r.url)
print(r.text)
# print(r.request.headers)