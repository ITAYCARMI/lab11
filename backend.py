import sqlite3
from flask import Flask, request, jsonify, abort
import math
import csv
import pandas as pd


app = Flask(__name__)
users = set()


############################## PART A ##############################


def init():
    """
    This method init the connection to db in part A
    """
    conn, cur = connect()
    create_store_table(conn, cur)
    read_csv()


def connect():
    """
    This method connect to demo database using sqlite3
    :return: connection, current cursor
    """
    conn = sqlite3.connect('demo.db')
    conn.text_factory = str
    current = conn.cursor()
    return conn, current


def create_store_table(conn, current):
    """
    This method create the movies table
    :param conn: connection of database
    :param current: current cursor
    """
    current.execute("create table if not exists Movies(id TEXT, title TEXT, genre TEXT)")
    conn.commit()
    conn.close()


def insert(id, title, genre):
    """
    This method insert movie in to movies table
    :param id: movie id that added
    :param title: movie title that added
    :param genre: movie genre that added
    """
    conn, cur = connect()
    cur.execute("insert into Movies values (?, ?, ?);", (id, title, genre))
    conn.commit()
    conn.close()


def delete(id, title, genre):
    """
    This method delete movie from movies table
    :param id: movie id that deleted
    :param title: movie title that deleted
    :param genre: movie genre that deleted
    """
    conn, cur = connect()
    with conn:
        cur.execute("DELETE FROM Movies WHERE id = ? and title = ? and genre = ?;", (id, title, genre))
        conn.commit()


def update(id, title, genre):
    """
    This method update movie details of movie in movies table
    :param id: movie id that updated
    :param title: movie title that updated
    :param genre: movie genre that updated
    """
    conn, cur = connect()
    with conn:
        cur.execute("UPDATE Movies SET title = ?, genre = ? WHERE id = ? ;", (title, genre, id))
        conn.commit()


def read_csv():
    """
    This method read details of movies from csv file
    """
    with open('movies.csv', mode='r') as movies:
        reader = csv.reader(movies)
        for row in reader:
            if not row[0] == 'movieId':
                id = row[0]
                title = row[1]
                genre = row[2].split("|")[0]
                insert(id, title, genre)
    movies.close()


def viewall():
    """
    This method shows the details of movies from data base
    :return: the rows in the data base
    """
    conn, cur = connect()
    with conn:
        cur.execute("SELECT  * FROM Movies")
        rows = cur.fetchall()
        return rows


def search_entry(id, title, genre):
    """
    This method help us to find movie in the data base
    :param id: movie id that searcher
    :param title: movie title that searcher
    :param genre: movie genre that searcher
    :return:
    """
    conn, cur = connect()
    with conn:
        cur.execute("SELECT  * FROM Movies WHERE id like ? and title like ? and genre like ?;",
                    ('%' + id + '%', '%' + title + '%', '%' + genre + '%',))
        rows = cur.fetchall()
        return rows


############################## PART B ##############################


def init_users():
    """
    This method init the connection to db in part B
    """
    connu, curu = connect_users()
    create_users_table(connu, curu)
    read_users_csv()


def connect_users():
    """
    This method connect to users database using sqlite3
    :return: connection, current cursor
    """
    conn = sqlite3.connect('users.db')
    conn.text_factory = str
    current = conn.cursor()
    return conn, current


def create_users_table(conn, current):
    """
    This method create the users table
    :param conn: connection of database
    :param current: current cursor
    """
    current.execute("create table if not exists users(userId INTEGER, movieId INTEGER, rating FLOAT)")
    conn.commit()
    conn.close()


def read_users_csv():
    """
    This method read details of users rating from csv file
    """
    global users
    with open('ratings.csv', mode='r') as ratings:
        reader = csv.reader(ratings)
        print ("start insert")
        for row in reader:
            if not row[0] == 'userId':
                user_id = row[0]
                movie_id = row[1]
                rating = row[2]
                insert_user(user_id, movie_id, rating)
                users.add(user_id)
    ratings.close()


def insert_user(user_id, movie_id, rating):
    """
    This method insert user in to users table
    :param user_id: user id that added
    :param movie_id: movie id that added
    :param rating: movie rating that added
    """
    conn, cur = connect_users()
    cur.execute("insert into users values (?, ?, ?);", (user_id, movie_id, rating))
    conn.commit()
    conn.close()


def recommend_movie(id, k):
    """
    This method control of recommending for user and k similar users
    :param id: user id that we recommend to him
    :param k: number of similar users, and k recommend movies
    :return: k movies that recommend to this user id
    """
    # init_users()
    global users
    list_recommended_users = find_similarity_users(id, k)
    return find_recommended_k_movies(list_recommended_users, k)


def init_users_set():
    """
    This method make the set from all the users
    """
    global users
    conn, cur = connect_users()
    cur.execute("SELECT userId FROM users;")
    for user in cur.fetchall():
        user_value = str(user).replace('\'', '')
        user_id = user_value[1:user_value.find(',')]
        users.add(user_id)


def find_similarity_users(id, k):
    """
    This method find k users that similar with this user id
    :param id: the user that we want to find him k similar users
    :param k: number of similar users
    :return: dictionary of similar users sorted by grade
    """
    global users
    conn, cur = connect_users()
    id_movies = {}
    grade_users = {}
    global users
    with conn:
        cur.execute("SELECT movieId, rating FROM users WHERE userId=? ;", (id,))
        for item in cur.fetchall():
            value = str(item).replace('\'', '')
            movie_id = value[1:value.find(',')]
            rating = value[value.find(',') + 1:value.find(')')]
            id_movies[movie_id] = rating
        users.remove(id)
        for user_id in users:
            user_movies = {}
            cur.execute("SELECT movieId, rating FROM users WHERE userId=? ;", (user_id,))
            for item in cur.fetchall():
                user_value = str(item).replace('\'', '')
                user_movie_id = user_value[1:user_value.find(',')]
                user_rating = user_value[user_value.find(',') + 1:user_value.find(')')]
                user_movies[user_movie_id] = user_rating
            grade_users[user_id] = users_calculation(id_movies, user_movies)
    sort_grade = sorted(grade_users, key=grade_users.get, reverse=True)
    return sort_grade


def users_calculation(id_movies, user_movies):
    """
    This method calculate the grade of specify user
    :param id_movies: movies dictionary of user id
    :param user_movies: movies dictionary of other user
    :return: grade of user
    """
    if len(set(id_movies.keys()) & set(user_movies.keys())) == 0:
        return 0
    average_rank_id_movies = float(sum(id_movies.values())) / len(id_movies)
    average_rank_user_movies = float(sum(user_movies.values())) / len(user_movies)
    mone = 0.0
    id_denominator = 0.0
    user_denominator = 0.0

    for movie_id in set(id_movies.keys() & user_movies.keys()):
        rank_id = float(id_movies[movie_id])
        rank_user = float(user_movies[movie_id])

        range_id = rank_id - average_rank_id_movies
        range_user = rank_user - average_rank_user_movies

        mone += (range_id * range_user)
        id_denominator += math.pow(range_id, 2)
        user_denominator += math.pow(range_user, 2)

    if id_denominator > 0 and user_denominator > 0:
        return mone / (math.pow(id_denominator, 0.5) * math.pow(user_denominator, 0.5))
    else:
        return 0


def find_recommended_k_movies(list_recommended_users, k):
    """
    This method return k recommended movies for the user id
    :param list_recommended_users: list of k similar users
    :param k: number of recommend movies
    :return: k recommended movies for the user id
    """
    conn, cur = connect_users()
    answer = []
    for user_id in list_recommended_users:
        user_movies = {}
        cur.execute("SELECT movieId, rating FROM users WHERE userId=? ;", (user_id,))
        for item in cur.fetchall():
            user_value = str(item).replace('\'', '')
            user_movie_id = user_value[1:user_value.find(',')]
            user_rating = user_value[user_value.find(',') + 1:user_value.find(')')]
            user_movies[user_movie_id] = user_rating
        sort_user_movies_id = sorted(user_movies, key=user_movies.get, reverse=True)
        for movie_id in sort_user_movies_id:
            if not answer.__contains__(movie_id):
                answer.append(movie_id)
                break
    return jsonify(answer[:int(k)])


@app.route('/', methods=['GET', 'POST'])
def web_service():
    """
    This method control of connection to the web service
    """
    global users
    init_users_set()
    if request.method == 'GET':
        id = request.values.get('userid')
        k = request.values.get('k')
        if users.__contains__(id) and k < len(users):
            return recommend_movie(id, k)
        else:
            abort(404)
            abort("thus values are invalids")
    else:
        value = request.values.get
        id = request.values.get('userid')
        k = request.values.get('k')
        if users.__contains__(id) and k < len(users):
            return recommend_movie(id, k)
        else:
            abort(404)
            abort("thus values are invalids")
        pass


if __name__ == '__main__':
    print "start"
    app.run(debug=True)
