import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import io
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(
    page_title="DWM Mini Project", page_icon=":bar_chart:"
)

import requests

url = "http://localhost:5054/make_ask"

def tenseconds():
    payload = ""
    headers = {
    'Access-Control-Allow-Origin': '*'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

placeholder = st.empty()
placeholder_cpu = st.empty()

for seconds in range(20):
    df = pd.read_csv(r"memory.csv") 
    df_cpu = pd.read_csv(r"cpu.csv")

    fig, ax = plt.subplots()

    lines = []
    for col in ["available", "free", "total", "used"]:
        line, = ax.plot([], [], label=col)
        lines.append(line)

    with placeholder.container():
        for i, col in enumerate(["available", "free", "total", "used"]):
            lines[i].set_data(df.index, df[col])

        # Set plot limits and labels
        ax.set_xlim(0, len(df))
        ax.set_ylim(0, df.max().max())  # Adjust based on your data
        ax.set_xlabel("Time")
        ax.set_ylabel("Memory Usage")
        ax.set_title("Real-Time Memory Usage Plot")

        # Display the plot in Streamlit
        st.pyplot(fig)

        # Wait for 10 seconds before updating again

    fig_cpu, ax_cpu = plt.subplots()
    lines_cpu = []

    for col in ["ctx_switches", "interrupts", "soft_interrupts", "syscalls"]:  # Adjusted columns
        line, = ax_cpu.plot([], [], label=col)
        lines_cpu.append(line)

    with placeholder_cpu.container():
        for i, col in enumerate(["ctx_switches", "interrupts", "soft_interrupts", "syscalls"]):  # Adjusted columns
            lines_cpu[i].set_data(df_cpu.index, df_cpu[col])
        ax_cpu.set_xlim(0, len(df_cpu))
        ax_cpu.set_ylim(0, df_cpu.max().max())  # Adjust based on your data (might need to change)
        ax_cpu.set_xlabel("Time")
        ax_cpu.set_ylabel("CPU Metrics")  # Adjusted label
        ax_cpu.set_title("Real-Time CPU Metrics")  # Adjusted title
        st.pyplot(fig_cpu)

    stats = tenseconds()
    time.sleep(10)