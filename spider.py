import requests

from domain import *
from general import *
from link_finder import *


class Spider(object):
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    video_player_urls_file = ''
    crawled_video_player_urls_file = ''
    video_urls_file = ''
    queue = set()
    crawled = set()
    video_player_urls = set()
    crawled_video_player_urls = set()
    video_urls = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.video_player_urls_file = Spider.project_name + '/video_player_urls.txt'
        Spider.crawled_video_player_urls_file = Spider.project_name + '/crawled_video_player_urls.txt'
        Spider.video_urls_file = Spider.project_name + '/video_urls.txt'
        self.boot()
        # self.crawl_all_urls('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        # 创建四个文件，其中queue文件中放入入口链接--base_url
        create_data_files(Spider.project_name, Spider.base_url)
        # queue和crawled作为类变量被所有实例共享
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_all_urls(thread_name, page_url):
        if page_url not in Spider.crawled:
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)) + '\n')
            print(thread_name + ' now crawling ' + page_url + '\n')
            urls, video_player_urls = Spider.gather_all_urls(page_url)
            Spider.add_urls_to_queue(urls)
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.video_player_urls.update(video_player_urls)
            set_to_file(Spider.queue, Spider.queue_file)
            set_to_file(Spider.crawled, Spider.crawled_file)
            set_to_file(Spider.video_player_urls, Spider.video_player_urls_file)

    @staticmethod
    def gather_all_urls(page_url):
        html_string = ''
        try:
            response = requests.get(page_url)
            if 'text/html' in response.headers['Content-Type']:
                html_string = response.text
            finder = LinkFinder(Spider.base_url, page_url)
            finder.find_all_urls(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.all_urls, finder.video_player_urls

    @staticmethod
    def add_urls_to_queue(urls):
        for url in urls:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def crawl_video_urls(thread_name, page_url):
        if page_url not in Spider.crawled_video_player_urls:
            print('Video player {0} | Video {1}\n'.format(str(len(Spider.video_player_urls)),
                                                          str(len(Spider.video_urls))))
            print(thread_name + ' now crawling ' + page_url + '\n')
            video_urls = Spider.gather_video_urls(page_url)
            Spider.video_urls.update(video_urls)
            Spider.crawled_video_player_urls.add(page_url)
            set_to_file(Spider.video_urls, Spider.video_urls_file)
            set_to_file(Spider.crawled_video_player_urls, Spider.crawled_video_player_urls_file)

    @staticmethod
    def gather_video_urls(page_url):
        html_string = ''
        try:
            response = requests.get(page_url)
            if 'text/html' in response.headers['Content-Type']:
                html_string = response.text
            finder = LinkFinder(Spider.base_url, page_url)
            finder.find_video_info(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.video_urls
