from app import ask
from flask_ask import statement, question
from flask_ask import session as ask_session, request as ask_request
import requests
from .weather import parse_weather

@ask.launch
def start_skill():
    welcome_message = 'Welcome would you like the air status for ' \
                      'your home or for a specific city?'
    reprompt_text = 'Say home or the name of a city and I will tell you the air quality and weather conditions'
    ask_session.attributes['last_speech'] = reprompt_text
    return question(welcome_message).reprompt(reprompt_text)

#need to check if 'have permission for post code, if not aks if still not then ask for city'


@ask.intent('CityAir')
def city_air(city, state):
    url = "http://api.airvisual.com/v2/city"
    querystring = {'city': city, 'state': state, 'country': 'USA',
                   "key": "YEa4b9c2pNdCTZpNp"}
    response = requests.request("GET", url, params=querystring).json()

    print(response)
    data = parse_weather(response)
    print(data)

    return question ('Current weather conditions are '+ data['conditions'] +
                     '. wind is blowing  ' + data['wind'] + 'with a spedd of '
                     + data['wind_speed'] + "the temperature is " + data['temp']
                     + ' with humidity ' + data['humidity'] + '. Air quality is '
                     + data['aqius'])