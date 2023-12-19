from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import psutil

cpu_warning_threshold = 80
cpu_critical_threshold = 95
mem_warning_threshold = 70
mem_critical_threshold = 90


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

def returnstats(given_server_name, server_addr):
    server_name = given_server_name
    server_ip = server_addr
    
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent()

    # Get memory usage
    mem_usage = psutil.virtual_memory().percent

    # Get additional memory information (optional)
    mem_stats = psutil.virtual_memory()

    # Optionally, get more detailed CPU information
    cpu_stats = psutil.cpu_stats()
    status = analyze_server_health(given_server_name=server_name, cpusage=cpu_usage, memusage=mem_usage)

    returnobj = {
        "Server Name": server_name,
        "Ip Address": server_ip,
        "CPU Usage": cpu_usage,
        "CPU Stats": cpu_stats,
        "Memory Usage": mem_usage,
        "Memory Stats": mem_stats,
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5053)
