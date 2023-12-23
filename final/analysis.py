"""Invoke engine.py for various assumptions used in your analysis"""

import requests

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

def main():
    conn: MySQLConnection = mysql.connector.connect(
        user="root", host="127.0.0.1", port="3306"
    )
    cursor: MySQLCursor = conn.cursor()

    engine_result = requests.get("http://localhost:8000/engine")

    query = ("INSERT INTO results VALUES engine_result = %s;")
    cursor.execute(query, engine_result)

    conn.close()

if __name__ == "__main__":
    main()