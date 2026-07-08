from flask import Flask, render_template, request
import re
import sqlite3
from datetime import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte_original TEXT,
            dates TEXT,
            montants TEXT,
            pourcentages TEXT,
            annees TEXT,
            telephones TEXT,
            autres_nombres TEXT,
            date_creation TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET", "POST"])
def home():
    texte = ""
    dates = []
    montants = []
    pourcentages = []
    annees = []
    telephones = []
    nombres = []

    if request.method == "POST":
        texte = request.form["texte"]

        dates = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", texte)

        montants = re.findall(
            r"\b\d+(?:[.,]\d+)?\s?(?:DT|TND|EUR|USD|€|\$|euros?)\b",
            texte,
            re.IGNORECASE
        )

        pourcentages = re.findall(
            r"\b\d+(?:[.,]\d+)?%",
            texte
        )

        annees = re.findall(r"\b(?:19|20)\d{2}\b", texte)

        telephones = re.findall(r"\b\d{8,12}\b", texte)

        texte_temp = texte

        for element in dates + montants + pourcentages + annees + telephones:
            texte_temp = texte_temp.replace(element, " ")

        nombres = re.findall(r"\b\d+\b", texte_temp)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO analyses (
                texte_original,
                dates,
                montants,
                pourcentages,
                annees,
                telephones,
                autres_nombres,
                date_creation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            texte,
            ", ".join(dates),
            ", ".join(montants),
            ", ".join(pourcentages),
            ", ".join(annees),
            ", ".join(telephones),
            ", ".join(nombres),
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    return render_template(
        "index.html",
        texte=texte,
        dates=dates,
        montants=montants,
        pourcentages=pourcentages,
        annees=annees,
        telephones=telephones,
        nombres=nombres
    )


@app.route("/historique")
def historique():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,
               texte_original,
               dates,
               montants,
               pourcentages,
               annees,
               telephones,
               autres_nombres,
               date_creation
        FROM analyses
        ORDER BY id DESC
    """)

    analyses = cursor.fetchall()

    conn.close()

    return render_template("historique.html", analyses=analyses)


if __name__ == "__main__":
    app.run(debug=True)