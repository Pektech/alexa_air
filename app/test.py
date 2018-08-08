#scratch file just to test api and stuff
import requests


'https://1jfmx0noqg.execute-api.us-east-1.amazonaws.com/dev'
def get_info():
    url = "http://api.airvisual.com/v2/city"

    querystring = {'city':'Springfield','country':'USA', "key":"YEa4b9c2pNdCTZpNp"}

    response = requests.request("GET", url, params=querystring)

    print(response.text)


response = {'status': 'success',
            'data': {'city': 'Albany', 'state': 'New York', 'country': 'USA',
            'location': {'type': 'Point', 'coordinates': [-73.7547, 42.6425]},
            'current': {'weather':
                            {'ts': '2018-08-04T00:00:00.000Z',
                             'hu': 83, 'ic': '10d', 'pr': 1020,
                             'tp': 21, 'wd': 160, 'ws': 3.6},
                        'pollution': {'ts': '2018-08-04T00:00:00.000Z', 'aqius': 19, 'mainus': 'o3', 'aqicn': 15, 'maincn': 'o3'}}}}




def get_latlong(zip):
    url = 'https://geocoder.api.here.com/6.2/geocode.json'
    querystring = {'app_id': 'ChfIK9R0Q9S8QEO9oC6V',
                   'app_code' : 'BI_N766MeUmLIgK3QYh93A', 'searchtext': zip,
                   'locationattributes': 'none,mapView'}
    feed = requests.request('GET', url, params=querystring)
    return feed.json()


test["Response"]['View'][0]['Result'][0]['Location']['DisplayPosition']
{'Latitude': 43.10176, 'Longitude': -73.5828}