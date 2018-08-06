from app import ask
from flask_ask import statement, question
from flask_ask import session as ask_session, request as ask_request, context
import requests
from .weather import GetWeatherData
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_model.ui import AskForPermissionsConsentCard
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.utils import is_request_type, is_intent_name
from geopy.geocoders import Nominatim


sb = CustomSkillBuilder(api_client=DefaultApiClient())
permissions = ["read::alexa:device:all:address:country_and_postal_code"]


def get_coordinates(location):
    geolocator = Nominatim(user_agent='alexa_air')
    coordinates = geolocator.geocode(location)
    print(coordinates.latitude, coordinates.longitude)

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



def get_alexa_location(deviceId, accessToken):
    URL = "https://api.amazonalexa.com/v1/devices/{}/settings" \
           "/address/countryAndPostalCode".format(context.System.device.deviceId)
    TOKEN = accessToken
    HEADER ={'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(TOKEN)}
    r = requests.get(URL, headers=HEADER)
    if r.status_code == 200:
        return  r.json()
    elif r.status_code == 403:
        return('need permission')


# class GetAddressHandler(AbstractRequestHandler):
#     def can_handle(self, handler_input):
#         return is_intent_name("GetAddressIntent")(handler_input)
#
#
#     def handle(self, handler_input):
#         req_envelope = handler_input.request_envelope
#         response_builder = handler_input.response_builder
#         service_client_fact = handler_input.service_client_factory
#
#         if not (req_envelope.context.system.user.permissions and
#                 req_envelope.context.system.user.permissions.consent_token):
#             response_builder.speak("I need your permission to access your zipcode"
#                                    " Please enable Location permissions in "
#                               "the Amazon Alexa app")
#             response_builder.set_card(
#                 AskForPermissionsConsentCard(permissions=permissions))
#             return response_builder.response



@ask.intent('GetAddressIntent')
def home():
    deviceID = context.System.device['deviceId']
    accessToken = context.System['apiAccessToken']
    print(deviceID)
    check_permission = get_alexa_location(deviceID, accessToken)
    print(check_permission)
    location = check_permission['postalCode']
    get_coordinates(location)

    return statement(check_permission['postalCode'])


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
