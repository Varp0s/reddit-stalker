from threading import Thread
from api.api_sv import run_api_server
from nw_sc.rd_Crawl import stalk as stalk_function

stalk_thread = Thread(target=stalk_function)
stalk_thread.start()


stalk_thread.join()

api_thread.join()
