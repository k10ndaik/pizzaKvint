import sqlite3
base = sqlite3.connect('baza.db')
cur = base.cursor()

base.execute('CREATE TABLE IF NOT EXISTS states(id PRIMARY KEY, state BLOB)')
base.commit()



