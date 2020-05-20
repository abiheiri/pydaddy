# pydaddy

A tool that leverages the [GoDaddy domains API](https://developer.godaddy.com/doc/endpoint/domains#/) so that you can make DNS changes without leveraging the website.

#### Requirements:
* Python v3+
* [requests](https://github.com/requests/requests) module


On MacOS, you can install the module like so:
    
    brew install pipenv
    pipenv install requests

You also need to create a credentials file
    
    echo "USER,PASS" > cred.conf



