from flask import Flask, render_template, request, jsonify
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
            cursor.execute("SELECT * FROM collection")
            cards = [row for row in cursor.fetchall()]
            return jsonify(cards), 200
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
