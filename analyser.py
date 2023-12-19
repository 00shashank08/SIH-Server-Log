from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import json
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

data = pd.read_csv("memory.csv")
data2 = pd.read_csv("cpu.csv")

@app.route("/analyse_mem", methods=["POST"])
@cross_origin()
def analyse_mem():
    global data

    # Calculate memory usage percentages
    data["used_pct"] = data["used"] / data["total"] * 100

    # Calculate IQR
    q1 = data["used_pct"].quantile(0.25)
    q3 = data["used_pct"].quantile(0.75)
    iqr = q3 - q1

    # data = data.drop("Unnamed: 0")

    # Identify outliers and their corresponding rows
    outlier_dict = {}
    for i, row in data.iterrows():
        if row["used_pct"] < (q1 - 1.5 * iqr) or row["used_pct"] > (q3 + 1.5 * iqr):
            outlier_dict[i] = row.to_dict()

    # Print outliers
    if outlier_dict:
        return {
            "Outliers: ": outlier_dict
        }
    else:
        return "No outliers found"

    # return str(data)
    
# Function to calculate Z-score
def z_score(x, mean, std):
    return (x - mean) / std

    
@app.route("/analyse_cpu", methods=["POST"])
@cross_origin()
def analyse_cpu():

    # Calculate percentiles for each metric
    q1 = data2.quantile(0.25)
    q3 = data2.quantile(0.75)

    # Calculate Interquartile Range (IQR) for each metric
    iqr = q3 - q1

    # Identify outliers based on IQR
    outliers = {}
    for col in data2.columns:
        for i in range(len(data2)):
            if data2.loc[i, col] < q1[col] - 1.5 * iqr[col] or data2.loc[i, col] > q3[col] + 1.5 * iqr[col]:
                outliers[f"index: {i}, metric: {col}"] = data2.loc[i, col]

    return outliers if outliers else "No outliers"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5056)

