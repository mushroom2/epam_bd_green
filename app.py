from flask import Flask, render_template, request
import requests
import json
import time

api_key = 'AIzaSyD7biSf5Aa5lUFmoDX2nYu8eGbsuzB1bY8'
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&type=point_of_interest&radius=1000&key={}'
next_page_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}'
# Lemberg
# y1 = 49.8696
# x1 = 23.9434
# y2 = 49.7705
# x2 = 24.1575

# rad = 1000

app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    return render_template('index.html')


def export_to_file(response):
    with open('output.json', 'w') as output_file:
        json.dump(response, output_file, skipkeys=True)
        output_file.close()


def get_poi(url, poi_storage, next_page=False):
    if next_page:
        print('### next page! ###')
    poi_response = requests.get(url)
    for poi in poi_response.json()['results']:
        if poi['id'] not in poi_storage:
            print(poi['id'], poi['name'])
            poi_storage[poi['id']] = poi
    if poi_response.json().get('next_page_token'):
        next_page = next_page_url.format(
            poi_response.json()['next_page_token'], api_key)
        time.sleep(2)  # token delay
        get_poi(next_page, poi_storage, True)


@app.route("/poi/get", methods=['GET', 'POST'])
def get_poi_by_coords():
    if request.method == 'POST':
        response_data = request.get_json(force=True)
        storage = {}

        print(response_data)
        y1 = float(response_data['lng_for'])
        x1 = float(response_data['lat_for'])
        y2 = float(response_data['lng_to'])
        x2 = float(response_data['lat_to'])

        while y1 > y2:
            while x1 < x2:
                get_poi(base_url.format(y1, x1, api_key), storage)
                print(y1, x1)
                x1 += 0.013
            print(y1)
            y1 -= 0.009
            x1 = 23.9434

        export_to_file(storage)
        return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
