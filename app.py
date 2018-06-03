from flask import Flask, render_template, request
import asyncio
from aiohttp import ClientSession
import json
#api_key = 'AIzaSyD7biSf5Aa5lUFmoDX2nYu8eGbsuzB1bY8'
api_key = 'AIzaSyDfL2zBB0klXRbrnr85Vy6SSR1fSAbgEiI'
# Lemberg
# y1 = 49.8696
# x1 = 23.9434
# y2 = 49.7705
# x2 = 24.1575

# rad = 1000
import os
app = Flask(__name__, static_url_path='')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/poi/get", methods=['GET', 'POST'])
def get_poi_by_coords():
    if request.method == 'POST':
        response_data = request.get_json(force=True)

        y1 = float(response_data['lng_for'])
        x1 = float(response_data['lat_for'])
        y2 = float(response_data['lng_to'])
        x2 = float(response_data['lat_to'])

        os.system('python get_google_poi.py {} {} {} {}'.format(y1, x1, y2, x2))
        return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)