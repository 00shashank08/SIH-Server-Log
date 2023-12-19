from flask import Flask, request, jsonify, url_for
from flask_cors import CORS, cross_origin
import json
import requests
import pandas as pd

import psutil

cpu_warning_threshold = 80
cpu_critical_threshold = 95
mem_warning_threshold = 70
mem_critical_threshold = 90

url = "http://localhost:5053/ask"

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

def analyze_server_health(given_server_name, cpusage, memusage):
  """
  Analyzes server health and returns a message based on CPU and memory usage.
  """
  server_name = given_server_name
  cpu_usage = cpusage
  mem_usage = memusage

  # Analyze CPU usage and define alert level
  alert_level, alert_message = ("OK", f"CPU usage on {server_name} is within normal range ({cpu_usage:.2f}%)")
  if cpu_usage > cpu_critical_threshold:
    alert_level, alert_message = "Critical", f"CPU usage on {server_name} ({cpu_usage:.2f}%) is exceeding critical threshold ({cpu_critical_threshold}%)!"
  elif cpu_usage > cpu_warning_threshold:
    alert_level, alert_message = "Warning", f"CPU usage on {server_name} ({cpu_usage:.2f}%) is approaching warning threshold ({cpu_warning_threshold}%)!"

  # Analyze memory usage and update alert level if necessary
  if mem_usage > mem_critical_threshold:
    alert_level = "Critical" if alert_level != "Critical" else "Critical (Both CPU & Memory)"
    alert_message += f"\nMemory usage on {server_name} ({mem_usage:.2f}%) is exceeding critical threshold ({mem_critical_threshold}%)!"
  elif mem_usage > mem_warning_threshold:
    alert_level = "Warning" if alert_level != "Critical" else "Warning (Both CPU & Memory)"
    alert_message += f"\nMemory usage on {server_name} ({mem_usage:.2f}%) is approaching warning threshold ({mem_warning_threshold}%)!"

  return {
    "status": alert_level,
    "message": alert_message,
  }

def returnstats_skeletal(given_server_name, server_addr):
  server_name = given_server_name
  server_ip = server_addr

  # Get CPU usage percentage
  cpu_usage = psutil.cpu_percent()

  # Get memory usage
  mem_usage = psutil.virtual_memory().percent

  disk_usage = psutil.disk_usage("/").percent
  network_bytes_sent, network_bytes_received = psutil.net_io_counters().bytes_sent, psutil.net_io_counters().bytes_recv

  returnobj = {
    "CPU Usage": cpu_usage,
    "disk_usage": disk_usage,
    "network_traffic": {
      "sent": network_bytes_sent,
      "received": network_bytes_received,
    },     
    "Memory Usage": mem_usage,
  }

  return returnobj


def returnstats(given_server_name, server_addr):
  server_name = given_server_name
  server_ip = server_addr
  
  # Get CPU usage percentage
  cpu_usage = psutil.cpu_percent()
  cpu_usage_num = psutil.cpu_percent()

  # Get memory usage
  mem_usage = psutil.virtual_memory().percent

  # Get additional memory information (optional)
  mem_stats = psutil.virtual_memory()

  # Optionally, get more detailed CPU information
  cpu_stats = psutil.cpu_stats()
  status = analyze_server_health(given_server_name=server_name, cpusage=cpu_usage_num, memusage=mem_usage)

  disk_usage = psutil.disk_usage("/").percent
  network_bytes_sent, network_bytes_received = psutil.net_io_counters().bytes_sent, psutil.net_io_counters().bytes_recv

  returnobj = {
      "Server Name": server_name,
      "Ip Address": server_ip,
      "CPU Usage": cpu_usage,
      "CPU Stats": {
        "ctx_switches":cpu_stats.ctx_switches,
        "interrupts":cpu_stats.interrupts,
        "soft_interrupts":cpu_stats.soft_interrupts,
        "syscalls":cpu_stats.syscalls
      },
      "disk_usage": disk_usage,
      "network_traffic": {
          "sent": network_bytes_sent,
          "received": network_bytes_received,
      },
      "Memory Usage": mem_usage,
      "Memory Stats": {
        "total": mem_stats.total,
        "used": mem_stats.used,
        "free": mem_stats.free,
        "available": mem_stats.available,
    },
      "Status": status
  }

  return returnobj


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/ask", methods=["POST"])
@cross_origin()
def ask():
    servername = request.json["server_name"]
    ip_addr = request.json["ip"]

    obj = returnstats(given_server_name=servername, server_addr=ip_addr)

    return obj

@app.route("/ask_skeletal", methods=["POST"])
@cross_origin()
def ask_skeletal():
    servername = request.json["server_name"]
    ip_addr = request.json["ip"]

    obj_sk = returnstats_skeletal(given_server_name=servername, server_addr=ip_addr)

    return obj_sk

@app.route("/make_ask", methods=["POST"])
@cross_origin()
def make_ask():
    # Extract data from incoming request
    data = request.json

    # Prepare data for the /ask route call
    server_name = data.get("server_name")
    ip_addr = data.get("ip_addr")

    # Check for mandatory data if necessary
    if not (server_name and ip_addr):
        # Handle missing data error
        return {"error": "Missing server_name or ip_addr"}, 400

    # Make a request to the /ask route using the extracted data
    target_url = url_for("ask", _external=True)  # Adjust based on routing setup
    response = requests.post(target_url, json=data)
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

    # Check for successful response
    if response.status_code == 200:
        # Return the received object from /ask
        return dict({
            "memory": str(newmem),
            "cpu": str(newcpu)
        })
    else:
        # Handle error from /ask (e.g., 404, internal server error)
        return {"error": f"Error from /ask: {response.status_code}"}, response.status_code



@app.route("/internal", methods=["POST"])
@cross_origin()
def internal():

    
    servername = request.json["server_name"]
    ip_addr = request.json["ip"]

    
    payload = {
        "server_name": servername,
        "ip": ip_addr
        }

    target_url = url_for("make_ask")
    
    response = requests.request("POST", url="http://127.0.0.1:5055/make_ask", headers=headers, data=payload)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5055)
