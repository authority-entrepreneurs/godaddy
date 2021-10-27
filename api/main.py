import json
import re

import requests
from flask import Flask, abort, request
from flask.json import jsonify

app = Flask(__name__)

secret = 'Jiwg84i5YngV4ujqeq99bh'
key = '9u51FqnVxbH_MsLGytZiRf7jSygtWvddnW'

auth_key = 'sso-key'+' '+key+':'+secret
test_base_url = 'https://api.ote-godaddy.com/'
prod_base_url = 'https://api.godaddy.com/'

regex = re.compile('@[!#$%^&*()<>?/\|}{~:]')


@app.route('/webhook/godaddy/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        sub_domain_name = request.args.get('sub_domain_name', None)
        if sub_domain_name is None:
            return "Sub domain name is not present"
        if not regex.search(sub_domain_name) == None:
            return "Only Special Character -, _, @ allowed"
        domain_name = 'dineline.co'
        port = 443

        data_format = [
                {
                    "data": "flash.funnels.msgsndr.com", #will be same always
                    "name": sub_domain_name, #different
                    "port": port, #what abt this one???
                    "priority": 0, # no need 
                    "protocol": "string", # no need
                    "service": "string", #no need
                    "ttl": 600, #will be same always
                    "type": "CNAME", # will be same always
                    "weight": 0 # no need
                }
            ]
        url = 'https://api.godaddy.com/v1/domains/{domain}/records'.format(domain=domain_name)
        headers = {"Authorization":auth_key}
        response = requests.patch(
            url, json=data_format, headers=headers
        )
        if response.status_code == 200:
            return {
                "msg":"sub domain name {0} on port {1} added for domain {2}".format(sub_domain_name, port, domain_name)
            }
        else:
            return {
                "msg":"Could not add sub domain name",
                "errors":response.json()
            }
    else:
        abort(400)
