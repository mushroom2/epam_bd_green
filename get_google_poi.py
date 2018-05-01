import requests


def get_struct(data):
    print(data['id'], data['name'])

api_key = 'AIzaSyD7biSf5Aa5lUFmoDX2nYu8eGbsuzB1bY8'
x1 = 49.8596
y1 = 23.8834
x2 = 49.8135
y2 = 24.0784
rad = 1000
#base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=49.8383,24.0232&keyword=poi&radius=1000&key={}'.format(api_key)
while x1 > x2:
    while y1 < y2:
        base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&keyword=poi&radius=1000&key={}'.format(
            x1, y1, api_key)
        r = requests.get(base_url)
        for i in r.json()['results']:
            get_struct(i)
        print(y1)
        y1 += 0.001
    print(x1)
    x1 -= 0.001


print(x1 - x2)
print(y1 - y2)