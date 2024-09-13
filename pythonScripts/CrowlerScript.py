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
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
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
        '_token': 'OesPv2gh9BPVdGzoY74gcvq9iWxq2GjG',  # Token from the original request
        '_leftlat': leftlat,
        '_rightlat': rightlat,
        '_toplng': toplng,
        '_bottomlng': bottomlng
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
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
        print(f"Response {index} saved as 'json_responses/response_{index}.json'.")

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
    print(lat_lng_pairs)
    return lat_lng_pairs

def main():
    min_lat = 36.0 
    max_lat = 37.0  
    min_lng = 49.0
    max_lng = 50.0  
    lat_step = 0.2  
    lng_step = 0.2

    latlng_grid = generate_latlng_grid(min_lat, max_lat, min_lng, max_lng, lat_step, lng_step)
    db_handler = SqlManager.DBHandler(user='root', password='rootpassword', host='localhost', database='travel_data')
    db_handler.connect()
    db_handler.create_table()

    locations = []  # Store all locations here
    request_counter = 0  # Track the number of requests made
    count = 1 
    while count < 5:
        for index, (leftlat, rightlat, toplng, bottomlng) in enumerate(latlng_grid):
            if count >= 5:  # Check if the count has reached 5
                break
            print(f"Fetching data for region {index + 1}: leftlat={leftlat}, rightlat={rightlat}, toplng={toplng}, bottomlng={bottomlng}")
            json_data = fetch_locations(leftlat, rightlat, toplng, bottomlng)
    
            if json_data:
                print(json_data)
                db_handler.insert_data(json_data)
                save_json_response(json_data, index + 1)
                parse_and_save_data(json_data, locations)
    
            count += 1 
            request_counter += 1
            if request_counter % 2 == 0:  # After every 2 requests
                print("Sleeping for 10 seconds to respect rate limit...")
                time.sleep(10)
            else:
                time.sleep(1)  # Shorter sleep for individual requests within the batch
    
    if locations:
        df = pd.DataFrame(locations)
        df.to_csv('all_locations_data.csv', index=False)
        print("Data saved to all_locations_data.csv")

# Run the main function
if __name__ == "__main__":
    main()

