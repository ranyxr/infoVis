import pandas as pd
from pathlib import Path
import requests
import re
import codecs
import json
from time import sleep
from copy import copy
from bs4 import BeautifulSoup


class Artist:
    def __init__(self, name):
        self.name = name
        self.born = None
        self.died = None
        self.nationality = None
        self.pic_url = None
        self.desc = None
        self.reference = None
        self.wiki_url = self.get_wiki_link()

    def get_wiki_link(self):
        base_url = 'https://en.wikipedia.org/wiki/'
        wiki_link = base_url + self.name.replace(' ', '_')
        return wiki_link


def read_from_parquet(dir_name):
    data_dir = Path(dir_name)
    full_df = pd.concat(
        pd.read_parquet(parquet_file)
        for parquet_file in data_dir.glob('*.parquet')
    )
    full_df.to_csv('wiki_artist.csv')


def get_html(csv_file):
    df = pd.read_csv(csv_file)
    artist = df[['name', 'html']].loc[df['html'] != '404'].to_dict('r')
    return artist


def parse_wiki(wiki_dict):
    artist = Artist(wiki_dict['name'])
    wiki_html_content = wiki_dict['html']
    soup = BeautifulSoup(wiki_html_content, features="html.parser")

    try:
        references = soup.findAll('div', attrs={'class': 'reflist'})
        if len(references) > 1:
            l1 = references[0].find('ol', attrs={'class': 'references'}).findAll('li')
            l2 = references[1].find('ol', attrs={'class': 'references'}).findAll('li')
            artist.reference = len(l1) + len(l2)
        else:
            l1 = references[0].find('ol', attrs={'class': 'references'}).findAll('li')
            artist.reference = len(l1)
    except Exception as e:
        print("ReferenceException", e, artist.name)

    text = soup.find('div', attrs={'class': 'mw-parser-output'}).findAll('p')
    desc = text[1].text + text[2].text
    attributes = soup.find('table', attrs={'class': 'infobox'}).findAll('tr')
    img = attributes[1].a['href']
    born = attributes[2].text.replace('Born', '')
    for attr in attributes[3:]:
        if 'Died' in attr.text:
            artist.died = attr.text.replace('Died', '')
        if 'Nationality' in attr.text:
            artist.nationality = attr.text.replace('Nationality', '')
    artist.born = born
    artist.desc = desc.strip('\n')
    artist.pic_url = artist.wiki_url + '#/media/' + re.match('.*(File.*)', img)[1]
    print(artist.__dict__)
    return artist.__dict__


if __name__ == '__main__':
    read_from_parquet('.')
    artist_list = get_html('wiki_artist.csv')
    artist_dict = {'artist': []}
    for artist in artist_list:
        try:
            artist_profile = parse_wiki(artist)
            artist_dict['artist'].append(artist_profile)
        except Exception as e:
            print('ParseException: ', e, artist['name'])

    with codecs.open('artists.json', 'w', 'utf-8') as f:
        f.write(json.dumps(artist_dict))

