import json

import requests
from flask import Flask, abort, request
from flask.json import jsonify

app = Flask(__name__)

secret = 'UeAJvdmQLoaHbzcdNvaA5K'
key = '3mM44Ubh7y4Mp5_HKWwFDHC9AGMqZVxBDiAEy'

auth_key = 'sso-key'+' '+key+':'+secret
test_base_url = 'https://api.ote-godaddy.com/'
prod_base_url = 'https://api.godaddy.com/'


@app.route('/webhook/godaddy/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        try:
            sub_domain_name = data.get('sub_domain_name', None)
        except Exception:
            return "Sub domain name is not present"
        try:
            domain_name = data.get('domain_name', None)
        except Exception:
            return "Domain name is not present"
        port = data.get('port', 443)

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
        url = 'https://api.ote-godaddy.com/v1/domains/{domain}/records'.format(domain=domain_name)
        headers = {"Authorization":auth_key}
        response = requests.patch(
            url, json=data_format, headers=headers
        )
        if response.status_code == 200:
            return {
                "msg":"sub domain name {0} on port {1} added for domain {2}".format(sub_domain_name, domain_name, port)
            }
        else:
            return {
                "msg":"Could not add sub domain name",
                "errors":response.json()
            }
    else:
        abort(400)
        



