from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    texte = ""

    dates = []
    montants = []
    annees = []
    telephones = []
    nombres = []

    if request.method == "POST":

        texte = request.form["texte"]

        dates = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", texte)

        montants = re.findall(
            r"\b\d+\s?(?:DT|TND|EUR|USD|€|\$)\b",
            texte,
            re.IGNORECASE
        )

        annees = re.findall(r"\b(?:19|20)\d{2}\b", texte)

        telephones = re.findall(r"\b\d{8}\b", texte)

        nombres = re.findall(r"\b\d+\b", texte)

    return render_template(
        "index.html",
        texte=texte,
        dates=dates,
        montants=montants,
        annees=annees,
        telephones=telephones,
        nombres=nombres
    )


if __name__ == "__main__":
    app.run(debug=True)