
import sqlite3
verbindung = sqlite3.connect ("Database.db")
zeiger = verbindung.cursor()
sql_anweisung = """
CREATE TABLE IF NOT EXISTS scans (
Produktnummer INTEGER(10),
Zeitpunkt DATETIME(30)
);"""
zeiger.execute(sql_anweisung)
verbindung.commit()
verbindung.close()
