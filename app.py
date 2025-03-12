from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    result = cur.fetchall()
    conn.close()
    return (result[0] if result else None) if one else result

@app.route("/inventory", methods=["GET"])
def get_inventory():
    artworks = query_db('SELECT "Engel nr.", Eksemplar, Titel, Serie, "Størrelse (cm)", Fysisk, "Pris (DKK)", Lokation, Status, År, Udstillinger, Kommentarer, Thumbnail FROM artwork')

    return jsonify([dict(row) for row in artworks])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

