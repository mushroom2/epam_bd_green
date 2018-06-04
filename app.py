import time

from flask import Flask, render_template, request
import requests
from multiprocessing.dummy import Pool as ThreadPool
import json
from math import cos, radians

api_key = 'AIzaSyDlNk0FBjkhaO719WZPSY9IA6zZvvEcpbQ'
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&type=point_of_interest&radius=1000&key={}'
next_page_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}'
# Lemberg
# y1 = 49.8696
# x1 = 23.9434


app = Flask(__name__, static_url_path='')
pool = ThreadPool(4)

@app.route("/")
def index():
    return render_template('index.html')


def export_to_file(storage):
    with open('output.json', 'w') as output_file:
        json.dump(storage, output_file, skipkeys=True)
        output_file.close()


def get_poi(url, poi_storage, next_page=False):
    poi_response = requests.get(url)
    if next_page and poi_response.json()['status'] == 'INVALID_REQUEST':
        print('### next page! ###')
        time.sleep(0.1)
        get_poi(url, poi_storage, True)
    for poi in poi_response.json()['results']:
        if poi['id'] not in poi_storage:
            print(poi['id'], poi['name'])
            poi_storage[poi['id']] = poi
    if poi_response.json().get('next_page_token'):
        next_page = next_page_url.format(
            poi_response.json()['next_page_token'], api_key)
        # time.sleep(2)  # token delay
        get_poi(next_page, poi_storage, True)


def find_and_save_poi_on_geo_coord_system(y_coord, x_coord, max_distance, key, storage):
    # central point of searching
    get_poi(base_url.format(y_coord, x_coord, key), storage)
    x_step = 0
    y_step = 1 / 110.574
    for distance_x in range(max_distance):
        for distance_y in range(max_distance):
            get_poi(base_url.format(y_coord + y_step, x_coord + x_step, key), storage)
            get_poi(base_url.format(y_coord - y_step, x_coord + x_step, key), storage)
            if x_step != 0:
                get_poi(base_url.format(y_coord + y_step, x_coord - x_step, key), storage)
                get_poi(base_url.format(y_coord - y_step, x_coord - x_step, key), storage)
            y_step += 1 / 110.574
        x_step += 1 / (110.574 * cos(radians(x_coord)))


@app.route("/poi/get", methods=['GET', 'POST'])
def get_poi_by_coords():
    if request.method == 'POST':
        response_data = request.get_json(force=True)
        storage = {}

        print(response_data)
        y1 = float(response_data['lng_for'])
        x1 = float(response_data['lat_for'])
        max_distance = int(response_data['distance'])

        find_and_save_poi_on_geo_coord_system(y1, x1, max_distance, api_key, storage)
        export_to_file(storage)
        return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
