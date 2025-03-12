# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd

# Indlæs CSV-filen med UTF-8 encoding og semikolon som separator
csv_file = "TEKST-Engle-Tabel 1.csv"  # Sørg for at filnavnet matcher præcist
df = pd.read_csv(csv_file, encoding="utf-8", sep=";", quotechar='"')

# Opret forbindelse til en SQLite-database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Opret en tabel (hvis den ikke allerede findes)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS artwork (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        No TEXT,
        Titel TEXT,
        Serie TEXT,
        Størrelse TEXT,
        Fysisk TEXT,
        Pris TEXT,
        Lokation TEXT,
        Status TEXT,
        År TEXT,
        Udstillinger TEXT,
        Kommentarer TEXT
    )
""")

# Indsæt data fra CSV i databasen
df.to_sql("artwork", conn, if_exists="replace", index=False)

# Luk forbindelsen
conn.commit()
conn.close()

print("✅ Data importeret til SQLite-databasen 'inventory.db'!")
