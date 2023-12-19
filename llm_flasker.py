from flask import Flask, request, jsonify
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

text_file = r"E:\Work\workbackups\localdata\apikey.txt"

with open(text_file, "r") as f:
    api_key = f.read().strip()

llm = OpenAI(openai_api_key=api_key)

conversation_history = ["Analyze web server logs, focusing on user login and logout activity. Analyse and report the total number of logins and logouts, potential security threats, and any login failures. On the basis of these logs, is it likely that there any possible attacks occuring?"]



@app.route("/chat", methods=["POST"])
@cross_origin()
def chat():
    global conversation_history
    logs = request.form["logs"]

    prompt = PromptTemplate(
        template=" ".join(conversation_history) + "\nQ: {question}\n A: ",
        input_variables=["question"],
    )

    question = "The logs are: " + str(logs)

    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run(question)

    return {
        "logs": logs,
        "evaluation": response,
        "history": conversation_history
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)