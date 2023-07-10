import sqlite3

def create_database():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            subreddit TEXT,
            url TEXT,
            author TEXT
        )
    """)
    conn.commit()
    conn.close()

def check_table_exists():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    conn.close()
    return 'posts' in table_names

create_database()


if check_table_exists():
    print("posts tablosu mevcut.")
else:
    print("posts tablosu mevcut değil.")
