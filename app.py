import asyncio
import time
from mysmallorm import get_dict_of_users
from aiohttp import ClientSession
from quart import Quart, render_template, request
import json
from math import cos, radians
api_key = 'AIzaSyAjh9FsfkEhyISZSfY-JND8zw52JztuKLg'
base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&type=point_of_interest&radius=1000&key={}'
next_page_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}'
# Lemberg
# y1 = 49.8696
# x1 = 23.9434


app = Quart(__name__, static_url_path='')
loop = asyncio.get_event_loop()


@app.route("/")
async def index():
    users = get_dict_of_users()
    return await render_template('index.html', users=users)


def export_to_file(storage):
    with open('output.json', 'w') as output_file:
        json.dump(storage, output_file, skipkeys=True)
        output_file.close()


async def get_poi(url):
    async with ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            return await response.json()


async def get_poi_from_next_page(results):
    tasks = []
    next_pages = [next_pages for next_pages in results if next_pages.get('next_page_token')]
    for next_page in next_pages:
        asyncio.sleep(1)
        tasks.append(get_poi(next_page_url.format(next_page['next_page_token'], api_key)))
    return await asyncio.gather(*tasks)


async def find_and_save_poi_on_geo_coord_system(y_coord, x_coord, max_distance, key):
    # central point of searching
    tasks = [get_poi(base_url.format(y_coord, x_coord, key))]
    x_step = 0
    for distance_x in range(max_distance):
        y_step = 1 / 110.574
        for distance_y in range(max_distance):
            tasks.append(get_poi(base_url.format(y_coord + y_step, x_coord + x_step, key)))
            tasks.append(get_poi(base_url.format(y_coord - y_step, x_coord + x_step, key)))
            if x_step != 0:
                tasks.append(get_poi(base_url.format(y_coord + y_step, x_coord - x_step, key)))
                tasks.append(get_poi(base_url.format(y_coord - y_step, x_coord - x_step, key)))
            y_step += 1 / 110.574
        x_step += 1 / (110.574 * cos(radians(y_coord)))
    return await asyncio.gather(*tasks)


@app.route("/poi/get", methods=['GET', 'POST'])
async def get_poi_by_coords():
    if request.method == 'POST':
        response_data = await request.get_json(force=True)
        ids = []
        storage = []

        print(response_data)
        y1 = float(response_data['lng_for'])
        x1 = float(response_data['lat_for'])
        max_distance = int(response_data['distance'])

        results = await find_and_save_poi_on_geo_coord_system(y1, x1, max_distance, api_key)
        time.sleep(2)
        results_from_second_page = await get_poi_from_next_page(results)
        time.sleep(2)
        results_from_third_page = await get_poi_from_next_page(results_from_second_page)

        for result in results + results_from_second_page + results_from_third_page:
            for poi in result['results']:
                if poi['id'] not in ids:
                    ids.append(poi['id'])
                    storage.append(poi)

        export_to_file(storage)
        return 'ok'


@app.route('/jsonresult')
def summary():
    with open('output.json') as f:
        res = json.load(f)
        response = app.response_class(
            response=json.dumps(res),
            status=200,
            mimetype='application/json'
        )
        return response


@app.route('/get_interest/user/<id>')
def get_interests():
    users = get_dict_of_users()
    response = app.response_class(
        response=json.dumps(users[int(id)]),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
