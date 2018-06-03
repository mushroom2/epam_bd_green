import json
import asyncio
from aiohttp import ClientSession
import sys
store = []
poikeys = []
api_key = 'AIzaSyDfL2zBB0klXRbrnr85Vy6SSR1fSAbgEiI'


# Lemberg
y1 = float(sys.argv[1])  # 49.8696
x1 = xbase = float(sys.argv[2])  # 23.9434
y2 = float(sys.argv[3])  # 49.7705
x2 = float(sys.argv[4])  # 24.1575

rad = 1000
cnt = 0


def export_to_file(d):
    with open('output.json', 'w') as outfile:
        json.dump(d, outfile)


async def get_poi(url, next_page=False):
    global cnt
    if next_page:
        print('### next page! ###')
    async with ClientSession() as session:
        async with session.get(url) as response:
            poi = await response.json()
            cnt += 1
            for i in poi['results']:
                if i['id'] not in poikeys:
                    print(i['id'], i['name'])
                    store.append(i)
                    poikeys.append(i['id'])
            if poi.get('next_page_token'):
                nextpageurl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={}&key={}'.format(
                    poi['next_page_token'], api_key)
                # time.sleep(2)  # token delay
                asyncio.sleep(2.0)
                get_poi(nextpageurl, True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = []
    while y1 > y2:
        while x1 < x2:
            base_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&type=point_of_interest&radius=1000&key={}'.format(
                y1, x1, api_key)
            task = asyncio.ensure_future(get_poi(base_url))
            tasks.append(task)
            print(y1, x1)
            x1 += 0.013
        print(y1)
        y1 -= 0.009
        x1 = xbase
    loop.run_until_complete(asyncio.wait(tasks))
    print('requests {} poi {}'.format(cnt, len(poikeys)))
    export_to_file(store)
