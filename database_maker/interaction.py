#from createDB import create_connection, create_table
import sqlite3


conn = sqlite3.connect("AciduleDB.db")

cur = conn.cursor()
cur.execute("""SHOW DATABASES""")