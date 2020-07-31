import sqlite3

verbindung = sqlite3.connect ("Database.db")
zeiger = verbindung.cursor()
zeiger.execute("DELETE FROM scans")
verbindung.commit()
inhalt = zeiger.fetchall()
print(inhalt)
verbindung.close()
