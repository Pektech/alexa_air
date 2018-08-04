#scratch file just to test api and stuff
import requests



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




def test_parse(response):