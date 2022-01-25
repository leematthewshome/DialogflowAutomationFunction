from flask import jsonify
import json
import requests

CONTROL_ROOM = 'https://yourcrname.my.automationanywhere.digital'
BOT_JSON = '{"fileId": 6560, "runAsUserIds": [55], "poolIds": [], "overrideDefaultDevice": false,  "botInput": { }}'
BOT_JSON = json.loads(BOT_JSON)
CR_USERNAME = 'your.username'
CR_PASSWORD = 'your.password'

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
    jsonpkg = '{"username": "' + CR_USERNAME + '", "password": "' + CR_PASSWORD + '"}'
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
    # Initial JSON response will only contain the deployment ID, which is not so useful for the user. When the bot finishes there will be outputs available to the user. 
    # The outputs can be retreived via the API with the deployment ID, but that is not a human friendly reference.
    # The cloud function should store a human friendly reference against each deployment ID and respond to the human user with the friendly reference (we have hard coded one below)
    # The user could then come back to the chatbot and enter the reference (via a different intent) to check up on the status of their request.
    
    responseText = "Thank you very much for all the information. Your application reference is MORT001034. One of our experienced home loan consultants will be in contact very soon. You can check on the status of your application in this chat panel. Just mention your application reference."
    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}
    return res
