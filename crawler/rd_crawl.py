import asyncio
import json
from playwright import async_api
import sqlite3
import time
from threading import Thread
from api.api_sv import run_api_server


api_info = [
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0",
        "browser_type": "firefox",
        "headless": True
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "browser_type": "chrome",
        "headless": True
    },
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0",
        "browser_type": "firefox",
        "headless": True
    }
]

username="changeme"

password="changeme"

def ignore_trace(*args):
    pass

async def main():
    subreddits = ["all"]  # Takip etmek istediğiniz subreddit listesi
    await stalk(subreddits)

async def login(page):
    await page.goto("https://www.reddit.com/login/")
    await page.fill("input[name='username']", username)
    await page.fill("input[name='password']", password)
    await page.press("input[name='password']", "Enter")
    time.sleep(5)


async def stalk(subreddits):
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS posts (id TEXT PRIMARY KEY, title TEXT, subreddit TEXT, url TEXT, author TEXT)')

    api_index = 0
    counter = 0

    while True:
        client_info = api_info[api_index]

        async with async_api.async_playwright() as p:
            browser_type = p.firefox
            browser = await browser_type.launch(headless=client_info["headless"])
            context = await browser.new_context(user_agent=client_info["user_agent"])
            page = await context.new_page()

            # Çerezleri kontrol et
            cookies_file = "cookies.json"
            try:
                with open(cookies_file, "r") as f:
                    cookies = json.load(f)
                await context.add_cookies(cookies)
            except FileNotFoundError:
                await login(page)
                cookies = await context.cookies()
                with open(cookies_file, "w") as f:
                    json.dump(cookies, f)

            for subreddit_name in subreddits:
                await page.goto(f"https://www.reddit.com/r/{subreddit_name}/new/")

                new_posts = await page.query_selector_all('div[data-testid="post-container"]')

                for post in new_posts:
                    post_url_element = await post.query_selector('a[data-click-id="body"]')
                    post_url = await post_url_element.get_attribute("href") if post_url_element else None
                    post_id = post_url.split('/')[-3] if post_url else None
                    post_title_element = await post.query_selector('h3')
                    post_title = await post_title_element.inner_text() if post_title_element else None
                    post_subreddit = subreddit_name
                    post_author_element = await post.query_selector('a[data-click-id="user"]')
                    post_author = await post_author_element.inner_text() if post_author_element else None

                    c.execute('INSERT OR IGNORE INTO posts (id, title, subreddit, url, author) VALUES (?, ?, ?, ?, ?)',
                            (post_id, post_title, post_subreddit, post_url, post_author))

                
                conn.set_trace_callback(ignore_trace)
                counter += 1
                if counter >= 3000:
                    time.sleep(2)
                    counter = 0
                conn.commit()

            await context.close()
            await browser.close()

        api_index = (api_index + 1) % len(api_info)

        time.sleep(3)

    conn.close()

api_thread = Thread(target=run_api_server)
api_thread.start()

asyncio.run(main())
