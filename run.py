from pymongo import MongoClient
import math
from flask import Flask, render_template, request

app = Flask(__name__)

# flask
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        inputMass = request.form["text"]
        if inputMass:
            #inputMass = int(inputMass)
            return render_template("calcMass.html", result = "re")
    return render_template("calcMass.html", result = "none")

if __name__ == "__main__":
    app.run()
