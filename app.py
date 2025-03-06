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
            text = card["flavorText"]
        else:
            text = ""
        c.execute(
            "INSERT INTO cardset (name, stage, energytype, image, text) VALUES (?,?,?,?,?)",
            (
                card["name"],
                card["subtypes"][0],
                card["types"][0],
                card["images"]["small"],
                text,
            ),
        )
    print("Added cards to cardset table")
    conn.commit()
    conn.close()
    # except sqlite3.Error as e:
    #     print("Error while connecting to SQLite database:", e)


@app.route("/", methods=["GET", "POST"])
def main():
    type_data = {
        "Colorless": 0,
        "Darkness": 0,
        "Dragon": 0,
        "Fighting": 0,
        "Fire": 0,
        "Grass": 0,
        "Lightning": 0,
        "Metal": 0,
        "Psychic": 0,
        "Water": 0,
    }
    if request.method == "POST":
        conn = sqlite3.connect("pokemon.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("""DROP TABLE IF EXISTS cardsearch""")
        c.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS cardsearch USING FTS5(id,name,stage,energytype,image,text)"
        )
        c.execute("INSERT INTO cardsearch SELECT * FROM cardset")
        desc = request.form.get("desc")
        name = request.form.get("name")
        # stage = request.form.get("stage")
        # energy_type = request.form.get("energy_type")
        # conn = sqlite3.connect("pokemon.db")
        # conn.row_factory = sqlite3.Row
        # c = conn.cursor()
        c.execute(
            "SELECT * FROM cardsearch WHERE text MATCH (?) AND name MATCH (?)",
            (
                desc,
                name,
            ),
        )
        results = [dict(row) for row in c.fetchall()]
        conn.close()
    else:
        conn = sqlite3.connect("pokemon.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM cardset")
        results = [dict(row) for row in c.fetchall()]
        conn.close()
    for card in results:
        energytype = card["energytype"]
        type_data[energytype] = type_data[energytype] + 1
    type_values = list(type_data.values())
    return render_template("base.html", results=results, type_values=type_values)


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


# @app.route("/results", methods=["POST", "GET"])
# def results():
#     if request.method == "POST":
#         stage = request.form.get("stage")
#         energy_type = request.form.get("energy_type")
#         conn = sqlite3.connect("pokemon.db")
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT * FROM cardset WHERE stage = (?) AND energytype = (?)",
#             (stage, energy_type),
#         )
#         cards = [dict(row) for row in cursor.fetchall()]
#     else:
#         conn = sqlite3.connect("pokemon.db")
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM cardset")
#         cards = [dict(row) for row in cursor.fetchall()]
#     return cards


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
