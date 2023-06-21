from threading import Thread
from api.api_sv import run_api_server
from stalker.stalker import stalk


subreddits = [
    "all"
]


api_thread = Thread(target=run_api_server)
api_thread.start()


stalk_thread = Thread(target=stalk, args=(subreddits,))
stalk_thread.start()


stalk_thread.join()
api_thread.join()
