from flask import Flask, render_template, request, jsonify
import requests
import sqlite3

app = Flask(__name__)


def get_set():
    try:
        response = requests.get(
            "https://api.pokemontcg.io/v2/cards?q=set.id:hgss3 supertype:pokemon"
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
        """CREATE TABLE IF NOT EXISTS cardset (id INTEGER PRIMARY KEY, name VARCHAR, stage VARCHAR, energytype VARCHAR, image VARCHAR, text VARCHAR)"""
    )
    print("Created cardset table")
    for card in cardset:
        if card.get("flavorText"):
            c.execute(
                "INSERT INTO cardset (name, stage, energytype, image, text) VALUES (?,?,?,?,?)",
                (
                    card["name"],
                    card["subtypes"][0],
                    card["types"][0],
                    card["images"]["small"],
                    card["flavorText"],
                ),
            )
        else:
            c.execute(
                "INSERT INTO cardset (name, stage, energytype, image) VALUES (?,?,?,?)",
                (
                    card["name"],
                    card["subtypes"][0],
                    card["types"][0],
                    card["images"]["small"],
                ),
            ),
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
    # elif request.method == "POST":
    #     try:
    #         new_card = request.args.get("card")
    #         cursor.execute("INSERT INTO collection (card) VALUES (?)", (new_card))
    #         conn.commit()
    #         conn.close()
    #         return jsonify({"message": "Card added successfully"}), 201
    #     except sqlite3.Error as e:
    #         return jsonify({"error": str(e)}, 500)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        stage = request.form.get("stage")
        energy_type = request.form.get("energy_type")
        conn = sqlite3.connect("pokemon.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM cardset WHERE stage = (?) AND energytype = (?)",
            (stage, energy_type),
        )
        cards = [dict(row) for row in cursor.fetchall()]
    else:
        conn = sqlite3.connect("pokemon.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cardset")
        cards = [dict(row) for row in cursor.fetchall()]
    return render_template("search.html", cards=cards)


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
