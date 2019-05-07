import sqlite3
from flask import Flask, request
# jasonify
import csv
import pandas as pd


app = Flask(__name__)


def init():
    conn, cur = connect()
    create_store_table(conn, cur)
    readCSV()



def connect():
    conn = sqlite3.connect('demo.db')
    conn.text_factory = str
    current = conn.cursor()
    return conn, current


def create_store_table(conn, current):
    current.execute("create table if not exists Movies(id TEXT, title TEXT, genre TEXT)")
    conn.commit()
    conn.close()


def insert(id, title, genre):
    conn, cur = connect()
    cur.execute("insert into Movies values (?, ?, ?);", (id, title, genre))
    conn.commit()
    conn.close()


#@app.route('/', methods=['GET', 'POST'])
def view():
    #request.form['username']
    conn, cur = connect()
    with conn:
        cur.execute("SELECT  * FROM Movies")
        rows = cur.fetchall()
        for row in rows:
            print(row)


def delete(item):
    conn, cur = connect()
    with conn:
        cur.execute("DELETE FROM Movies WHERE item = ?", (item,))
        conn.commit()


def update(q, p, item):
    conn, cur = connect()
    with conn:
        cur.execute("UPDATE Movies SET quantity = ?, price = ? WHERE item = ?;", (q, p, item,))
        conn.commit()


def readCSV():
    with open('movies.csv', mode='r') as movies:
        reader = csv.reader(movies)
        for row in reader:
            if not row[0] == 'movieId':
                id = row[0]
                title = row[1]
                genre = row[2].split("|")[0]
                insert(row[0], row[1], row[2].split("|")[0])

    movies.close()



#if __name__ == '__main__':
#    app.run(debug=True)


def viewall():
    conn, cur = connect()
    with conn:
        cur.execute("SELECT  * FROM Movies")
        rows = cur.fetchall()
        return rows


def search_entry(id, title, year):
    conn, cur = connect()
    with conn:
        cur.execute("SELECT  * FROM Movies WHERE id like ? and title like ?;", (id,'%'+year+'%',))
        rows = cur.fetchall()
        return rows
