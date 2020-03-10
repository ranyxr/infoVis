"""
Collect information about famous artists on Wikipedia.
"""
import threading
import requests
import re
import codecs
import json
from time import sleep
from copy import copy
from bs4 import BeautifulSoup

g_mutex = threading.Condition()
artist_queue = {'artist': []}


class Artist:
    def __init__(self, name):
        self.name = name
        self.born = None
        self.died = None
        self.nationality = None
        self.pic_url = None
        self.desc = None
        self.wiki_url = self.get_wiki_link()

    def get_wiki_link(self):
        base_url = 'https://en.wikipedia.org/wiki/'
        wiki_link = base_url + self.name.replace(' ', '_')
        return wiki_link


class Crawler:
    def __init__(self, artist_list, threadnum):
        self.artist_list = artist_list
        self.threadnum = threadnum
        self.threadpool = []

    def craw(self):
        i = 0
        while i < len(self.artist_list):
            tid = 0
            while tid < self.threadnum and i+tid < len(self.artist_list):
                self.download(self.artist_list[i+tid], tid)
                tid += 1
            i += tid
            for thread in self.threadpool:
                thread.join(30)

    def download(self, artist, tid):
        crawthread = CrawlerThread(artist, tid)
        self.threadpool.append(crawthread)
        crawthread.start()


class CrawlerThread(threading.Thread):
    def __init__(self, artist, tid):
        threading.Thread.__init__(self)
        self.artist = Artist(artist)
        self.tid = tid
        self.url = self.artist.wiki_url

    def run(self):
        global g_mutex

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
        }
        try:
            r = requests.get(self.url, headers=headers)
        except requests.exceptions.ConnectionError:
            sleep(60)
            r = requests.get(self.url, headers=headers)

        if r.status_code == 429:
            sleep(60)
            r = requests.get(self.url, headers=headers)
        if r.status_code == 404:
            return

        if not self.filter_artist(r.text):
            return
        try:
            self.parse_wiki(r.text)
        except Exception as e:
            print("ParseException: ", e, self.url)
            return
        g_mutex.acquire()
        print("Thread", self.tid, " is crawling ", self.url)
        self.save_to_queue()
        g_mutex.release()

    def filter_artist(self, wiki_html_content):
        soup = BeautifulSoup(wiki_html_content, features="html.parser")
        # filter out famous artists according to the number of references
        refer_num = 0
        try:
            references = soup.findAll('div', attrs={'class': 'reflist'})
            if len(references) > 1:
                l1 = references[0].find('ol', attrs={'class': 'references'}).findAll('li')
                l2 = references[1].find('ol', attrs={'class': 'references'}).findAll('li')
                refer_num = len(l1) + len(l2)
            else:
                l1 = references[0].find('ol', attrs={'class': 'references'}).findAll('li')
                refer_num = len(l1)
        except Exception as e:
            print("FilterException", e, self.url)
            return False
        if refer_num < 5:
            return False
        return True

    def parse_wiki(self, wiki_html_content):
        soup = BeautifulSoup(wiki_html_content, features="html.parser")

        text = soup.find('div', attrs={'class': 'mw-parser-output'}).findAll('p')
        desc = text[1].text + text[2].text
        attributes = soup.find('table', attrs={'class': 'infobox'}).findAll('tr')
        img = attributes[1].a['href']
        born = attributes[2].text.replace('Born', '')
        for attr in attributes[3:]:
            if 'Died' in attr.text:
                self.artist.died = attr.text.replace('Died', '')
            if 'Nationality' in attr.text:
                self.artist.nationality = attr.text.replace('Nationality', '')
        self.artist.born = born
        self.artist.desc = desc.strip('\n')
        self.artist.pic_url = self.url + '#/media/' + re.match('.*(File.*)', img)[1]
        print(self.artist.__dict__)

    def save_to_queue(self):
        global artist_queue
        artist_queue['artist'].append(self.artist.__dict__)


def load_artists(file_name):
    # artist names with special characters will be ignored.
    with codecs.open(file_name, 'r', 'utf-8') as f:
        artist_list = f.read().replace("'", '').strip('[]').split(', ')
    artist_set = set(artist_list)
    artist_set.remove("Unknown")
    artist_clean = copy(artist_set)
    for name in artist_set:
        # remove one-word name
        if ' ' not in name:
            artist_clean.remove(name)
    print(len(artist_clean), 'artists in total.')
    return list(artist_clean)


if __name__ == "__main__":
    threadnum = 30
    artist_list = load_artists('artists.txt')
    crawler = Crawler(artist_list, threadnum)
    crawler.craw()
    with open('artists.json', 'w') as f:
        f.write(json.dumps(artist_queue))