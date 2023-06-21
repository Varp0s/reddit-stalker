from flask import Flask, jsonify, g
import sqlite3
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

DATABASE = 'posts.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/posts")
def get_posts():
    conn = get_db()
    c = conn.cursor()

    c.execute('SELECT * FROM posts')
    posts = c.fetchall()

    c.close()

    formatted_posts = []
    for post in posts:
        formatted_posts.append({
            'id': post['id'],
            'title': post['title'],
            'subreddit': post['subreddit'],
            'url': post['url'],
            'author': post['author']
        })

    return jsonify(formatted_posts), 200, {'Content-Type': 'application/json; charset=utf-8'}

def run_api_server():
    with app.app_context():
        conn = get_db()
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS posts (id TEXT PRIMARY KEY, title TEXT, subreddit TEXT, url TEXT, author TEXT)')

        conn.commit()
        c.close()

    app.run(host='0.0.0.0', port=1453, debug=True, use_reloader=False)

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    log_file = 'api.log'
    file_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger('')
    logger.addHandler(file_handler)

    run_api_server()
