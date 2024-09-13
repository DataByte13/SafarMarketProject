import requests
import pandas as pd
import time
import json
import os
import random
import SqlManager  

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    
    'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/604.1',
    
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/18.19042',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 OPR/75.0.3969.279',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
]

def fetch_locations(leftlat, rightlat, toplng, bottomlng):
    url = 'https://safarmarket.com/blog/map/items'
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://safarmarket.com/blog/map',
        'Origin': 'https://safarmarket.com',
        'Connection': 'keep-alive'
    }
    data = {
        '_token': 'OesPv2gh9BPVdGzoY74gcvq9iWxq2GjG', 
        '_leftlat': leftlat,
        '_rightlat': rightlat,
        '_toplng': toplng,
        '_bottomlng': bottomlng
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 429:  
        print("warning , rich 429 , too many request  , lets sleep for 30 second !")
        time.sleep(30)
        return fetch_locations(leftlat, rightlat, toplng, bottomlng) 
    elif response.status_code in [500, 503]:
        print("Server error 500 or 503. we are  in the trubble !!!! Iam going for 2 min nap -> zzzz")
        time.sleep(120)
        return fetch_locations(leftlat, rightlat, toplng, bottomlng) 
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def parse_and_save_data(json_data, locations):
    if isinstance(json_data, list):
        for value in json_data:
            if isinstance(value, dict):  
                location = {
                    'SafarMarketID': value.get('id', None),
                    'Title': value.get('title', None),
                    'Description': value.get('description', None),
                    'Latitude': value.get('lat', None),
                    'Longitude': value.get('lng', None),
                    'Type': value.get('type', None),
                    'Image': value.get('main_image', None),
                    'Slug': value.get('slug', None),
                    'Rate': value.get('rate', None),
                    'RateCount': value.get('ratecount', None)
                }
                locations.append(location)
    else:
        print("Error: Expected a list of locations.")

def save_json_response(json_data, index):
    if json_data:
        if not os.path.exists('json_responses'):
            os.makedirs('json_responses')

        with open(f'json_responses/response_{index}.json', 'w') as f:
            json.dump(json_data, f, indent=4)
        #print(f"Response {index} saved as 'json_responses/response_{index}.json'.")

def generate_latlng_grid(min_lat, max_lat, min_lng, max_lng, lat_step, lng_step):
    lat_lng_pairs = []
    lat = min_lat
    while lat < max_lat:
        lng = min_lng
        while lng < max_lng:
            leftlat = lat
            rightlat = lat + lat_step
            toplng = lng + lng_step
            bottomlng = lng
            lat_lng_pairs.append((leftlat, rightlat, toplng, bottomlng))
            lng += lng_step
        lat += lat_step
    return lat_lng_pairs

def show_progress(completed, total,insertCounter, width=50,):
    percent = (completed / total) * 100
    progress = int(percent / 100 * width)
    bar = '=' * progress + '-' * (width - progress)
    print(f"Progress: [{bar}] {percent:.2f}% {insertCounter} data inserted into database")

def main():
    ''' Tehran Location
    min_lat = 35.5
    max_lat = 35.9
    min_lng = 51.2
    max_lng = 51.8
    '''
    min_lat = 24.0
    max_lat = 40.0
    min_lng = 44.0
    max_lng = 63.0
    lat_step = 0.05
    lng_step = 0.05
    latlng_grid = generate_latlng_grid(min_lat, max_lat, min_lng, max_lng, lat_step, lng_step)

    db_handler = SqlManager.DBHandler(user='root', password='rootpassword', host='localhost', database='Locations_DataBase')
    db_handler.connect()
    db_handler.create_table()

    locations = []  
    request_counter = 0  
    count = 1 
    
    total_requests = len(latlng_grid)
    requests_done = 0

    while True:
        for index, (leftlat, rightlat, toplng, bottomlng) in enumerate(latlng_grid):
            print(f"Fetching data for region {index + 1}: leftlat={leftlat}, rightlat={rightlat}, toplng={toplng}, bottomlng={bottomlng}")
            json_data = fetch_locations(leftlat, rightlat, toplng, bottomlng)
    
            if json_data:
                print(json_data)
                db_handler.insert_data(json_data)
                save_json_response(json_data, index + 1)
                parse_and_save_data(json_data, locations)
    
            count += 1 
            request_counter += 1
            requests_done += 1
            show_progress(requests_done, total_requests , db_handler.insert_status())
            if request_counter % 2 == 0:  
                time.sleep(5)
            else:
                time.sleep(1)  
            if count == 100 :
                time.sleep(300)
        break
    
    if locations:
        df = pd.DataFrame(locations)
        df.to_csv('all_locations_data.csv', index=False)
        print("Data saved to all_locations_data.csv")
if __name__ == "__main__":
    main()


