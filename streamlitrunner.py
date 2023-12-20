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



# # Define the function that generates a graph from the CSV file
# def generate_graph():
#     # Create a figure and axis object
#     fig, ax = plt.subplots()

#     # Plot the lines
#     ax.plot(df['available'], label='available')
#     ax.plot(df['free'], label='free')
#     ax.plot(df['total'], label='total')
#     ax.plot(df['used'], label='used')

#     # Set the title and axis labels
#     ax.set_title('Server Statistics')
#     ax.set_xlabel('Time')
#     ax.set_ylabel('Memory Usage')

#     # Add a legend
#     ax.legend()

#     # Display the plot
#     st.pyplot(fig=fig)

fig, ax = plt.subplots()

lines = []
for col in ["available", "free", "total", "used"]:
    line, = ax.plot([], [], label=col)
    lines.append(line)

def run():
    while True:
        stats = tenseconds()
        # Read the updated data from the CSV file (replace with your actual data retrieval method)
        new_data = pd.read_csv(r"E:\neov_ide\sih\SIH---Server-Log-\memory.csv")

        # Update the data for each line
        for i, col in enumerate(["available", "free", "total", "used"]):
            lines[i].set_data(new_data.index, new_data[col])

        # Set plot limits and labels
        ax.set_xlim(0, len(new_data))
        ax.set_ylim(0, new_data.max().max())  # Adjust based on your data
        ax.set_xlabel("Time")
        ax.set_ylabel("Memory Usage")
        ax.set_title("Real-Time Memory Usage Plot")

        # Display the plot in Streamlit
        st.pyplot(fig)

        # Wait for 10 seconds before updating again
        time.sleep(10)
        st.empty()

if __name__ == '__main__':
    container = st.container()
    with container:
        run()