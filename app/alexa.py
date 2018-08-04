from app import ask
from flask_ask import statement, question
from flask_ask import session as ask_session, request as ask_request
import requests
from .weather import GetWeatherData

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

    data = GetWeatherData(city, state)
    print(data)

    return question('Current weather conditions are '+ data.conditions[1] +
                     '. Wind is blowing  ' + data.wind_dir + ' with a speed of '
                     + data.wind_speed + " miles per second. the temperature is " + data.temp
                     + ' with humidity at' + data.humidity + '. Air quality index is '
                     + data.aqi[0] + ' which is ' + data.aqi[2])