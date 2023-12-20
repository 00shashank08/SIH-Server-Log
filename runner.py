from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import time
import requests
import json

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

headers = {
  'Access-Control-Allow-Origin': '*',
  'Content-Type': 'application/json'
}

# MAKE CHANGES HERE 
#  |   |   |
#  v   v   v
servers = ['localhost']

while True:
    #asker
    for server in servers:
        url = "http://" + server + ":5054/make_ask"
        payload = json.dumps({
            "server_name": "Myserver",
            "ip": "192.168.0.146"
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        if response:
            json_response = json.loads(response.text)
        
        if not response:
            url2 = "http://" + server + ":5056/analyse_cpu"
            url3 = "http://" + server + ":5056/analyse_mem"

            payload = json.dumps({
                "server_name": "Myserver",
                "ip": "192.168.0.146"
            })
            response2 = requests.request("POST", url2, headers=headers, data=payload)
            response3 = requests.request("POST", url3, headers=headers, data=payload)

            if str(response2) != "No outliers" or str(response3) != "No outliers found":
                url4 = "http://192.168.74.1:3600/notify"
                payload = json.dumps({
                    "Outliers_cpu": str(response2),
                    "Outliers_mem": str(response3)
                })

                print(payload)
                # response4 = requests.request("POST", url2, headers=headers, data=payload)

            #if no reply, `
        #outliers
        #if outliers,
        #hit email 192 168 74 1 3600 /notify 
                
    print("Running...........")

    time.sleep(10)