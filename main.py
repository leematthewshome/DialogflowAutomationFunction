from flask import jsonify
import json
import requests

CONTROL_ROOM = 'https://leemelbourne.my.automationanywhere.digital'
BOT_JSON = '{"fileId": 6560, "runAsUserIds": [55], "poolIds": [], "overrideDefaultDevice": false,  "botInput": { }}'
BOT_JSON = json.loads(BOT_JSON)

def main_function(request):

    request_json = request.get_json()
   
    #get the values required from the submitted JSON
    loanType = request_json["queryResult"]["outputContexts"][0]["parameters"]["mortgage-type"]
    name = request_json["queryResult"]["outputContexts"][0]["parameters"]["applicant-name"]
    amount = request_json["queryResult"]["outputContexts"][0]["parameters"]["loan-amount"]
    customer = request_json["queryResult"]["outputContexts"][0]["parameters"]["existing-customer"]
    account = request_json["queryResult"]["outputContexts"][0]["parameters"]["account-number"]
    phone = request_json["queryResult"]["outputContexts"][0]["parameters"]["phone-number"]
    
    #add the values to the bot deploy json
    BOT_JSON["botInput"]["loanType"] = {"type": "STRING", "string": loanType }
    BOT_JSON["botInput"]["name"] = {"type": "STRING", "string": name }
    BOT_JSON["botInput"]["amount"] = {"type": "STRING", "string": amount }
    BOT_JSON["botInput"]["customer"] = {"type": "STRING", "string": customer }
    BOT_JSON["botInput"]["account"] = {"type": "STRING", "string": account }
    BOT_JSON["botInput"]["phone"] = {"type": "STRING", "string": phone }
    
    #get token to access control room
    jsonpkg = '{"username": "my.username", "password": "my.password"}'
    endpoint = '/v1/authentication'
    headers = {'Content-Type': 'application/json'}  
    url = CONTROL_ROOM + endpoint
    result = requests.post(url=url, headers=headers, data=jsonpkg, verify=True) 
    data = result.json()
    token = data["token"]

    #submit the bot deploy request
    headers = '{"Content-Type": "application/json", "X-Authorization": "' + token + '"}'
    headers = json.loads(headers)
    endpoint = '/v3/automations/deploy'
    url = CONTROL_ROOM + endpoint
    jsonpkg = json.dumps(BOT_JSON)
    result = requests.post(url=url, headers=headers, data=jsonpkg, verify=True) 
    data = result.json()

    return data
