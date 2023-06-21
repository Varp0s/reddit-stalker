import praw
import sqlite3
import time

api_info = [
    {
        "client_id": "changeme",
        "client_secret": "changeme",
        "username": "changeme",
        "password": "changeme",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0"
    },
    {
        "client_id": "changeme",
        "client_secret": "changeme",
        "username": "changeme",
        "password": "changeme",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    },
    {
        "client_id": "changeme",
        "client_secret": "changeme",
        "username": "changeme",
        "password": "changeme",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0"
    }
]

def stalk(subreddits):
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (id TEXT PRIMARY KEY, title TEXT, subreddit TEXT, url TEXT, author TEXT)')

    api_index = 0
    counter = 0

    while True:
        client_info = api_info[api_index]

        reddit = praw.Reddit(
            client_id=client_info["client_id"],
            client_secret=client_info["client_secret"],
            username=client_info["username"],
            password=client_info["password"],
            user_agent=client_info["user_agent"]
        )

        for subreddit_name in subreddits:
            subreddit = reddit.subreddit(subreddit_name)
            new_posts = subreddit.new(limit=None)

            for post in new_posts:
                post_id = post.id
                post_title = post.title
                post_subreddit = subreddit_name
                post_url = post.url
                post_author = post.author.name if post.author else None

                c.execute('INSERT OR IGNORE INTO posts (id, title, subreddit, url, author) VALUES (?, ?, ?, ?, ?)',
                          (post_id, post_title, post_subreddit, post_url, post_author))

            conn.commit()

            counter += 1
            if counter >= 1000:
                time.sleep(10)
                counter = 0

        api_index = (api_index + 1) % len(api_info)

        time.sleep(20)  

        c.execute('SELECT * FROM posts')
        posts = c.fetchall()
        print(posts)  

    conn.close()
