from flask import Flask, jsonify, request
import sqlite3
import re  # Importér regex-modul for bedre rensning af prisen

app = Flask(__name__)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect("inventory.db")  # Sørg for at matche din databasefil
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    
    conn.commit()  # Sikrer at ændringer gemmes
    conn.close()
    
    return (rows[0] if rows else None) if one else rows


@app.route("/inventory", methods=["GET"])
def get_inventory():
    results = query_db("SELECT * FROM artwork")
    cleaned_results = []

    for row in results:
        row_dict = dict(row)
        
        # Debug: Print original pris
        if row_dict.get("Pris (DKK)"):
            original_price = row_dict["Pris (DKK)"]
            cleaned_price = re.sub(r"[^\d]", "", original_price)  # Fjerner alt, der ikke er tal
            
            print(f"Original pris: {original_price}", flush=True)  # Debug print    
            print(f"Renset pris: {cleaned_price}", flush=True)  # Debug print


            row_dict["Pris (DKK)"] = cleaned_price
        
        cleaned_results.append(row_dict)

    return jsonify(cleaned_results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
