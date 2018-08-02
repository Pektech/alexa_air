#scratch file just to test api and stuff

import requests

url = "http://api.airvisual.com/v2/city"

querystring = {'city':'Bancho','state':'Kagawa','country':'Japan', "key":"YEa4b9c2pNdCTZpNp"}

response = requests.request("GET", url, params=querystring)

print(response.text)