import re
from urllib import parse

from bs4 import BeautifulSoup


class LinkFinder(object):
    def __init__(self, base_url, page_url):
        self.base_url = base_url
        self.page_url = page_url
        self.all_urls = set()
        self.video_urls = set()
        self.video_player_urls = set()

    @staticmethod
    def make_soup(html_string):
        soup = BeautifulSoup(html_string, "html.parser")
        return soup

    # 获取网页上的所有链接
    def find_all_urls(self, html_string):
        pattern = re.compile(r'http://feidieshuo.com/media/play/[\d]+')
        soup = LinkFinder.make_soup(html_string)
        for a in soup.find_all('a', href=True):
            url = parse.urljoin(self.base_url, a['href'])
            self.all_urls.add(url)
            # 获取视频播放器链接
            if re.match(pattern, url):
                self.video_player_urls.add(url)

    # 获取播放器网址上对应的MP4链接
    def find_video_info(self, html_string):
        # 第一个pattern不严谨
        # pattern = re.compile(r'([\w]*)/([\d]*[\.]*[\w]*[\：]*[\:]*[\，]*[\,]*[\w]*[\？]*[\?]*).mp4')
        pattern = re.compile(r'mp4/([\S]*)/([\s]*[\S]*[\s]*).mp4')
        soup = LinkFinder.make_soup(html_string)
        # title = soup.find(attrs={'class': 't-word-text'}).text
        player_info = soup.find(attrs={'class': 'player-video-left',
                                       'id': 'player'}).find(attrs={'type': 'text/javascript'}).text.strip()
        category = re.findall(pattern, player_info)[0][0]
        title = re.findall(pattern, player_info)[0][1]
        url = 'http://video.feidieshuo.com/mp4/{0}/{1}.mp4'.format(category, title)
        self.video_urls.add(url)
