"""
Collect information about famous artists on Wikipedia.
"""
import threading
import requests
import re
import codecs
import os
import json
from datetime import datetime
from time import sleep
from copy import copy
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
import pyarrow


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

# --------------------------------------------------------------------------------------------

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',}
request_continue = True
file_artists_txt = 'artists.txt'
file_artists_parquet = '{}.parquet.gzip'
html_fetch_count = 0





# def udf_wiki_request(name):
#     global html_fetch_count
#     global request_continue
#     if request_continue is False:
#         return ""
#     url = 'https://en.wikipedia.org/wiki/'
#     url = url + name.replace(' ', '_')
#     try:
#         r = requests.get(url, headers=headers)
#         if r.status_code == 200:
#             r = r.text
#         elif r.status_code == 404:
#             r = "404"
#         elif r.status_code == 301:
#             r = "301"
#         elif r.status_code == 429:
#             request_continue = False
#             return ""
#         else:
#             request_continue = False
#             return ""
#     except requests.exceptions.ConnectionError:
#         request_continue = False
#         return ""
#     html_fetch_count += 1
#     return r


def load_artists():
    if os.path.exists(file_artists_parquet):
        r_df = pd.read_parquet(file_artists_parquet)
        print("{} [System]: {} artists in parquet file loaded.".format(datetime.now(), r_df.shape[0]))
    else:
        # artist names with special characters will be ignored.
        with codecs.open(file_artists_txt, 'r', 'utf-8') as f:
            artist_list = f.read().replace("'", '').strip('[]').split(', ')
        artist_set = set(artist_list)
        artist_set.remove("Unknown")
        r_df = pd.DataFrame(list(artist_set), columns=['name'])
        r_df['html'] = ''
        r_df.to_parquet(file_artists_parquet, compression='gzip')
        print("{} [System]: {} artists reads in.".format(datetime.now(), r_df.shape[0]))
    return r_df







        # in_df = pd.merge(in_df, t_df, on="name", how="outer", suffixes=('_',''))
        #
        # print(in_df.head(1))
        # in_df = in_df.merge(t_df, on='name', how='outer')
        # # pd.option_context('display.max_rows', None)
        # print(in_df.to_string())
        # t_df = in_df[in_df['html'] == ''].head(30)

# def run(self):
#         global g_mutex
#
#         try:
#             r = requests.get(self.url, headers=headers)
#         except requests.exceptions.ConnectionError:
#             sleep(60)
#             r = requests.get(self.url, headers=headers)
#
#         if r.status_code == 429:
#             sleep(60)
#             r = requests.get(self.url, headers=headers)
#         if r.status_code == 404:
#             return
#
#         if not self.filter_artist(r.text):
#             return
#         try:
#             self.parse_wiki(r.text)
#         except Exception as e:
#             print("ParseException: ", e, self.url)
#             return
#         g_mutex.acquire()
#         print("Thread", self.tid, " is crawling ", self.url)
#         self.save_to_queue()
#         g_mutex.release()


def udf_filter_artists(name):
    return name.replace(" ", "").isalpha() and (name.count(' ') < 3) and (' ' in name)


class Spider:
    def __init__(self):
        self.df = pd.DataFrame()
        self.process_flag = True
        self.row_group_num = 100
        self.wait_seconds = 60
        self.parquet_list = glob("./*.parquet.gzip")
        self.__initial_artists()

    def __udf_wiki_request(self, row):
        if row["html"] != "":
            return row["html"]
        if self.process_flag is False:
            print("{} [System]: The host is forbidden by Wikipedia. Wait {} seconds"
                  .format(datetime.now(), self.df.shape[0]), self.wait_seconds)
            sleep(self.wait_seconds)
            self.process_flag = True
        url = 'https://en.wikipedia.org/wiki/'
        url = url + row["name"].replace(' ', '_')
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                r = r.text
            elif r.status_code == 404:
                r = "404"
            elif r.status_code == 301:
                r = "301"
            elif r.status_code == 429:
                self.process_flag = False
                return ""
            else:
                self.process_flag = False
                return ""
        except requests.exceptions.ConnectionError:
            self.process_flag = False
            return ""
        return r

    @staticmethod
    def __to_parquet(df, parquet_id, parquet_name=""):
        fn = file_artists_parquet.format(parquet_id)
        if parquet_name is not "":
            fn = parquet_name
        df.to_parquet(fn, compression='gzip')
        print("{} [System]: {} saved.".format(datetime.now(), fn.format(parquet_id)))

    def __filter_artists(self):
        self.df["filter"] = self.df['name'].apply(udf_filter_artists)
        self.df = self.df[self.df["filter"]].reset_index(drop=True)
        self.df.drop('filter', axis=1, inplace=True)
        print("{} [System]: {} artists after filter.".format(datetime.now(), self.df.shape[0]))

    def __initial_artists(self):
        if len(self.parquet_list) > 0:
            return
        else:
            # Load data from disk
            # artist names with special characters will be ignored.
            with codecs.open(file_artists_txt, 'r', 'utf-8') as f:
                artist_list = f.read().replace("'", '').strip('[]').split(', ')
            # Clean artist names
            artist_set = set(artist_list)
            artist_set.remove("Unknown")
            self.df = pd.DataFrame(list(artist_set), columns=['name'])
            self.__filter_artists()
            self.df['html'] = ''
            print("{} [System]: {} artists reads in.".format(datetime.now(), self.df.shape[0]))
            # Split the data frame and save them as parquet
            count = 0
            while self.df.shape[0] > self.row_group_num:
                Spider.__to_parquet(self.df[:self.row_group_num], count)
                count += 1
                self.df = self.df[self.row_group_num:]
            Spider.__to_parquet(self.df[:self.row_group_num], count)
            self.parquet_list = glob("./*.parquet.gzip")

    def wiki_request(self):
        for par_file in self.parquet_list:
            print("{} [System]: Start to request {} from Wikipedia".format(datetime.now(), par_file))
            self.df = pd.read_parquet(par_file)
            while self.df[self.df['html'] == ''].size > 0:
                self.df["html"] = self.df.apply(self.__udf_wiki_request, axis=1)
            Spider.__to_parquet(self.df, 0, par_file)


if __name__ == "__main__":
    spider = Spider()
    spider.wiki_request()
    # spider = Spider()
    # spider.wiki_request()
    #
    # if df.shape[0] > 10:  # len(df) > 10 would also work
    #     first_ten = df[:10]
    #     rest = df[10:]
