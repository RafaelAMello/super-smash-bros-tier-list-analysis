import re
import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from app.models import Brawler

logging.basicConfig(level=logging.INFO)

def get_brawler(player_url, rank):
    logging.info(f"Requesting Page {player_url} Rank {rank}")
    soup = BeautifulSoup(requests.get(player_url).text, "lxml")
    player_data = {
        'url' : player_url,
        'updated_at' : datetime.strptime(soup.find('time')['datetime'], '%Y-%m-%dT%X+00:00'),
        'name' : soup.find('span', {'class' : 'pogo-name-alt'}).text,
        'rank' : rank,
        'image_url_large' : soup.find('img', {'class' : 'champion-icon-img featured-img'})['src'],
        'image_url_small' : soup.find('img', {'class' : 'alt-costume-ssbu'})['src'] if soup.find('img', {'class' : 'alt-costume-ssbu'}) else None
    }

    labels = [
        'weight',
        'air_speed',
        'fall_speed',
        'run_speed',
        'dash_speed'
    ]
    measurements = soup.find('table', {'class' : 'stats_table_new'}).find_all('div', {'class' : re.compile(r'hor_line ')})


    for label, measurement in zip(labels, measurements):
        player_data[label] = float(re.search(r'calc\((\d*\.?\d*)', measurement['style']).group(1))

    labels = [
        'universe',
        'tier'
    ]

    for label, measurement in zip(labels, soup.find('div', {'class' : 'upper-section-stats'}).find_all('div', {'class' : 'badge-text-above Rock'})):
        player_data[label] = measurement.text
        
    return Brawler(**player_data)

def get_brawlers_by_ranking():
    url = 'https://rankedboost.com/super-smash-bros/nintendo-switch-best-character/'
    soup = BeautifulSoup(requests.get(url).text, "lxml")

    for rank, player_url in enumerate(soup.find('div', {'class' : 'gg'}).find_all('a')):
        get_brawler(player_url['href'], rank + 1).save()

def get_brawler_counter(brawler):
    soup = BeautifulSoup(requests.get(brawler.url).text, "lxml")
    for counter in soup.find('div', {'id' : 'Matchups'}).find_all('div', {'class' : re.compile(r"mix")}):
        counter_brawler = Brawler.nodes.first(url=counter.find('a')['href'])
        counter_brawler.counters.connect(brawler)

def get_brawlers_counters():
    for brawler in Brawler.nodes.all():
        logging.info(f"Getting Counter for {brawler.name}")
        get_brawler_counter(brawler)

def get_brawlers_and_counters():
    get_brawlers_by_ranking()
    get_brawlers_counters()
