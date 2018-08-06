from app import ask
from flask_ask import statement, question
from flask_ask import session as ask_session, request as ask_request, context
import requests
from .weather import GetWeatherData

from geopy.geocoders import Nominatim

permissions = ["read::alexa:device:all:address:country_and_postal_code"]


def get_coordinates(location):
    geolocator = Nominatim(user_agent='alexa_air')
    coordinates = geolocator.geocode(location)
    return (coordinates.latitude, coordinates.longitude)


def get_alexa_location(deviceId, accessToken):
    URL = "https://api.amazonalexa.com/v1/devices/{}/settings" \
          "/address/countryAndPostalCode".format(
        context.System.device.deviceId)
    TOKEN = accessToken
    HEADER = {'Accept': 'application/json',
              'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(URL, headers=HEADER)
    if r.status_code == 200:
        return ('success', r.json())
    elif r.status_code == 403:
        return ('error')


@ask.launch
def start_skill():
    welcome_message = 'Welcome would you like the air status for ' \
                      'your location or for a specific city?'
    reprompt_text = 'Say home or the name of a city and I will tell you the ' \
                    'air quality and weather conditions'
    ask_session.attributes['last_speech'] = reprompt_text
    return question(welcome_message).reprompt(reprompt_text)


# need to check if 'have permission for post code, if not aks if still not
# then ask for city'


@ask.intent('GetAddressIntent')
def home():
    deviceID = context.System.device['deviceId']
    accessToken = context.System['apiAccessToken']
    check_permission = get_alexa_location(deviceID, accessToken)
    if check_permission[0] == 'success':
        location = check_permission[1]['postalCode']
        get_coordinates(location)
        return statement(check_permission['postalCode'])
    elif check_permission == 'error':
        return statement("I need your permission to access your zipcode."
                         " Please enable Location permissions in "
                         "the Alexa app"). \
            consent_card(
            'read::alexa:device:all:address:country_and_postal_code')


@ask.intent('CityAir')
def city_air(city, state):
    data = GetWeatherData(city, state)
    print(data)

    return question('Current weather conditions are ' + data.conditions[1] +
                    '. Wind is blowing  ' + data.wind_dir + ' with a speed of '
                    + data.wind_speed + " miles per second. the temperature "
                                        "is " + data.temp
                    + ' with humidity at' + data.humidity + '. Air quality '
                                                            'index is '
                    + data.aqi[0] + ' which is ' + data.aqi[2])
