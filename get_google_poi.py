import requests
store = []
poikeys = []
from mysmallorm import SqliteConnector
import json
import time

def export_to_file(d):
    with open('output.json', 'w') as outfile:
        json.dump(d, outfile)


api_key = 'AIzaSyD7biSf5Aa5lUFmoDX2nYu8eGbsuzB1bY8'

# Lemberg
y1 = 49.8696
x1 = 23.9434
y2 = 49.7705
x2 = 24.1575

rad = 1000


def get_poi(url, next_page=False):
    if next_page:
        print('### next page! ###')
    poi = requests.get(url)
    for i in poi.json()['results']:
        if i['id'] not in poikeys:
            print(i['id'], i['name'])
            store.append(i)
            poikeys.append(i['id'])
    if poi.json().get('next_page_token'):
        nextpageurl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}'.format(
            poi.json()['next_page_token'], api_key)
        time.sleep(2)  # token delay
        get_poi(nextpageurl, True)


while y1 > y2:
    while x1 < x2:
        base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&type=point_of_interest&radius=1000&key={}'.format(
            y1, x1, api_key)
        get_poi(base_url)
        print(y1, x1)
        x1 += 0.013
    print(y1)
    y1 -= 0.009
    x1 = 23.9434

export_to_file(store)