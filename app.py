from flask import Flask, redirect, render_template, request, url_for, jsonify
import requests
import sqlite3

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("base.html")


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("pokemon.sqlite")
    except sqlite3.Error as e:
        print("Error while connecting to SQLite database:", e)
    return conn


@app.route("/collection", methods=["GET", "POST"])
def collection():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        try:
            return render_template("collection.html")
            # cursor.execute("SELECT * FROM collection")
            # cards = [row for row in cursor.fetchall()]
            # return jsonify(cards), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == "POST":
        try:
            new_card = request.args.get("card")
            cursor.execute("INSERT INTO collection (card) VALUES (?)", (new_card))
            conn.commit()
            return jsonify({"message": "Card added successfully"}), 201
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}, 500)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form.get("search")
    try:
        response = requests.get(
            "https://api.pokemontcg.io/v2/cards?pageSize=10&q=name:{name}".format(
                name=search_term
            )
        )
        if response.status_code == 200:
            cards = response.json()["data"]
    except:
        cards = {}
    return render_template("search.html", cards=cards)
