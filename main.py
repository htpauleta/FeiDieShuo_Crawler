import threading
from queue import Queue

from domain import *
from general import *
from spider import Spider

PROJECT_NAME = 'feidieshuovideo'
HOMEPAGE = 'http://feidieshuo.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
VIDEO_PLAYER_URLS_FILE = PROJECT_NAME + '/video_player_urls.txt'
NUMBER_OF_THREAD = 8
# crawl all urls queue
queue0 = Queue()
# crawl video player info queue
queue1 = Queue()
# spider初始化
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


def create_workers():
    for _ in range(int(NUMBER_OF_THREAD / 2)):
        t = threading.Thread(target=work0)
        t.daemon = True
        t.start()
    for _ in range(int(NUMBER_OF_THREAD / 2), NUMBER_OF_THREAD):
        t = threading.Thread(target=work1)
        t.daemon = True
        t.start()


# crawl all urls
def work0():
    while True:
        url = queue0.get()
        Spider.crawl_all_urls(threading.current_thread().name, url)
        queue0.task_done()


# crawl video urls
def work1():
    while True:
        url = queue1.get()
        Spider.crawl_video_urls(threading.current_thread().name, url)
        queue1.task_done()


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue0.put(link)
    queue0.join()
    for link in file_to_set(VIDEO_PLAYER_URLS_FILE):
        queue1.put(link)
    queue1.join()
    crawl()


def crawl():
    if len(file_to_set(QUEUE_FILE)) > 0:
        print(str(len(file_to_set(QUEUE_FILE))) + ' url in the queue\n')
        create_jobs()

create_workers()
create_jobs()
