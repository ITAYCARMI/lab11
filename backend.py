import sqlite3
from flask import Flask, jasonify, request
from pip._vendor.urllib3 import request

app = Flask(__name__)

def connect():
    conn = sqlite3.connect('demo.db')
    current = conn.cursor()
    return conn, current


def create_store_table(conn, current):
    current.execute("create table if not exists store(item TEXT, quantity INTEGER, price REAL)")
    conn.commit()
    conn.close()


def insert(item, q, p):
    conn, cur = connect()
    cur.execute("insert into store values (?, ?, ?);", (item, q, p))
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def view():
    request.form['username']
    conn, cur = connect()
    with conn:
        cur.execute("SELECT  * FROM store")
        rows = cur.fetchall()
        for row in rows:
            print(row)


def delte(item):
    conn, cur = connect()
    with conn:
        cur.execute("DELETE FROM store WHERE item = ?", (item,))
        conn.commit()


def update(q, p, item):
    conn, cur = connect()
    with conn:
        cur.execute("UPDATE store SET quantity = ?, price = ? WHERE item = ?;", (q, p, item,))
        conn.commit()


if __name__ == '__main__':
    app.run(debug=True)
