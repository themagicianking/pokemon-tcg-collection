from flask import Flask, redirect, render_template, request, url_for, jsonify
import requests
import sqlite3

app = Flask(__name__)


def get_set():
    try:
        response = requests.get(
            "https://api.pokemontcg.io/v2/cards?set.name:HS—Undaunted"
        )
        if response.status_code == 200:
            cards = response.json()["data"]
            return cards
        else:
            return "Error fetching card set."
    except BaseException:
        return "Could not connect to API."


def create_database():
    # try:
    cardset = get_set()
    conn = sqlite3.connect("pokemon.db")
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS cardset""")
    c.execute(
        """CREATE TABLE IF NOT EXISTS cardset (id INTEGER PRIMARY KEY, name VARCHAR, type VARCHAR, image VARCHAR)"""
    )
    print("Created cardset table")
    for card in cardset:
        c.execute(
            "INSERT INTO cardset (name, type, image) VALUES (?,?,?)",
            (card["name"], card["types"][0], card["images"]["small"]),
        )
    print("Added cards to cardset table")
    conn.commit()
    conn.close()
    # except sqlite3.Error as e:
    #     print("Error while connecting to SQLite database:", e)


@app.route("/")
def main():
    return render_template("base.html")


@app.route("/collection", methods=["GET", "POST"])
def collection():
    conn = sqlite3.connect("pokemon.db")
    cursor = conn.cursor()

    if request.method == "GET":
        try:
            cursor.execute("SELECT * FROM cardset")
            cards = cursor.fetchall()
            conn.close()
            return jsonify(cards), 200
            # return render_template("collection.html", cards=cards)
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    elif request.method == "POST":
        try:
            new_card = request.args.get("card")
            cursor.execute("INSERT INTO collection (card) VALUES (?)", (new_card))
            conn.commit()
            conn.close()
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


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
