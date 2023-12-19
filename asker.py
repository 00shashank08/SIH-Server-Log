import requests
import json

url = "http://localhost:5053/ask"

payload = json.dumps({
  "server_name": "Myserver",
  "ip": "192.168.0.146"
})
headers = {
  'Access-Control-Allow-Origin': '*',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

text = response.text

# print(text)
json_response = json.loads(text)

print(json_response)
print("-------------------------")
print(json_response["Memory Usage"])
print(json_response["Memory Stats"])