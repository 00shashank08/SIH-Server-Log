from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import json
import pandas as pd

import psutil

url = "http://localhost:5053/ask"

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

mem_df = pd.DataFrame(columns=["available", "free", "total", "used"])
cpu_df = pd.DataFrame(columns=["ctx_switches", "interrupts", "soft_interrupts", "syscalls"])

def update_df(og_df, new_df):
    og_df = pd.concat([og_df, new_df], ignore_index=True)
    return og_df

payload = json.dumps({
  "server_name": "Myserver",
  "ip": "192.168.0.146"
})
headers = {
  'Access-Control-Allow-Origin': '*',
  'Content-Type': 'application/json'
}

@app.route("/make_ask", methods=["POST"])
@cross_origin()
def make_ask():
  global mem_df
  global cpu_df

  response = requests.request("POST", url, headers=headers, data=payload)
  json_response = json.loads(response.text)
  mem_stats = json_response["Memory Stats"]
  cpu_stats = json_response["CPU Stats"]

  # memdict = {
  #   "total": mem_stats.total,
  #   "used": mem_stats.used,
  #   "free": mem_stats.free,
  #   "available": mem_stats.available,
  # }

  # cpudict = {
  #   "ctx_switches":cpu_stats.ctx_switches,
  #   "interrupts":cpu_stats.interrupts,
  #   "soft_interrupts":cpu_stats.soft_interrupts,
  #   "syscalls":cpu_stats.syscalls
  # } 

  index = range(0, 1)
  newmem = pd.DataFrame(mem_stats, index=index)

  index2 = range(0, 1)
  newcpu = pd.DataFrame(cpu_stats, index=index2)

  mem_df = update_df(og_df=mem_df, new_df=newmem)
  cpu_df = update_df(og_df=cpu_df, new_df=newcpu)

  mem_df.to_csv("memory.csv")
  cpu_df.to_csv("cpu.csv")

  # return json_response
  # return str(str(type(mem_stats)) + " - " + str(mem_stats))
  return {
    "memory": str(mem_df),
    "cpu": str(cpu_df)
  }

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5054)