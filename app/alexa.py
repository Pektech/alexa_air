from app import ask
from flask_ask import statement, question
from flask_ask import session as ask_session, request as ask_request, context
import requests
from .weather import GetWeatherData, GetZipWeather, get_coordinates
from flask import url_for


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
    welcome_message = 'Welcome would you like the air status & weather for ' \
                      'your location or for a specific city?'
    reprompt_text = 'Say home or the name of a city & State and I will tell ' \
                    'you the ' \
                    'air quality and weather conditions'
    ask_session.attributes['last_speech'] = reprompt_text
    return question(welcome_message).reprompt(reprompt_text)


@ask.intent('GetAddressIntent')
def here():
    deviceID = context.System.device['deviceId']
    accessToken = context.System['apiAccessToken']
    check_permission = get_alexa_location(deviceID, accessToken)
    if check_permission[0] == 'success':
        location = check_permission[1]['postalCode']
        zipweatherdata = zipweather(location)
        return zipweatherdata
    elif check_permission == 'error':
        return statement("I need your permission to access your zipcode."
                         " Please enable Location permissions in "
                         "the Alexa app"). \
            consent_card(
            'read::alexa:device:all:address:country_and_postal_code')


@ask.intent('CityAir')
def city_air(city, state):
    data = GetWeatherData(city, state)
    status = data.status
    if status[0] != 'success':
        if status[1] == 'city_not_found':
            return question(
                "I'm sorry I could not find that city. You can repeat the "
                "name and state or if you say zipcode and "
                "the number I can find the nearest report")
        else:
            return statement(
                "I'm sorry the service is noy available at this time."
                "Please try later. Good Bye")
    forecast = 'Current weather conditions are ' + data.conditions[1] + \
               '. Wind is blowing  ' + data.wind_dir + ' with a speed of ' \
               + data.wind_speed + " miles per second. the temperature " \
                                   "is " + data.temp \
               + ' with humidity at ' + data.humidity + '. Air quality ' \
                                                        'index is ' \
               + data.aqi[0] + ' which is ' + data.aqi[2]

    display = context.System.device.supportedInterfaces.Display
    response = 'Weather is {}, Temp = {}'.format(data.conditions[1], data.temp)
    textContent = {'primaryText': {'type': 'RichText', 'text': response}}
    if display == None:
        return statement(forecast) \
            .standard_card(title='{}'.format(data.conditions[1]),
                           text='Air Quality  {}, Temp = {}'.format(
                               data.aqi[2], data.temp)
                           ,
                           small_image_url='https://737b52e8.ngrok.io/static'
                                           '/images/{}.png'
                           .format(data.conditions[0]))
    else:
        return statement(forecast)\
            .display_render(template='BodyTemplate2',
                            title='Air Quality {}'.
                            format(data.aqi[2]),
                            text=textContent,
                            image='https://737b52e8.ngrok.io/static/images/{}.png'
                             .format(data.conditions[0]))


@ask.intent('ZipAir', )
def zipweather(zip):
    data = GetZipWeather(zip)
    status = data.status
    if status[0] != 'success':
        if status[1] == 'city_not_found':
            return question(
                "I'm sorry I could not find that city. You can repeat the "
                "name and state or if you say zipcode and "
                "the number I can find the nearest report")
        else:
            return statement(
                "I'm sorry the service is noy available at this time."
                "Please try later. Good Bye")
    forecast = 'Current weather conditions are ' + data.conditions[1] + \
               '. Wind is blowing  ' + data.wind_dir + ' with a speed of ' \
               + data.wind_speed + " miles per second. the temperature " \
                                   "is " + data.temp \
               + ' with humidity at ' + data.humidity + '. Air quality ' \
                                                        'index is ' \
               + data.aqi[0] + ' which is ' + data.aqi[2]

    display = context.System.device.supportedInterfaces.Display
    response = 'Weather is {}, Temp = {}'.format(data.conditions[1], data.temp)
    textContent = {'primaryText': {'type': 'RichText', 'text': response}}
    if display == None:
        return statement(forecast) \
            .standard_card(title='{}'.format(data.conditions[1]),
                           text='Air Quality  {}, Temp = {}'.format(
                               data.aqi[2], data.temp)
                           ,
                           small_image_url='https://737b52e8.ngrok.io/static'
                                           '/images/{}.png'
                           .format(data.conditions[0]))
    else:
        return statement(
            forecast).display_render(
            template='BodyTemplate2',
            title='Air Quality {}'.format(data.aqi[2]),
            text=textContent,
            image='https://737b52e8.ngrok.io/static/images/{}.png'
            .format(data.conditions[0]))


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.intent('AMAZON.NoIntent')
def goodbye():
    return statement('Good bye')

@ask.intent('AMAZON.HelpIntent')
def help():
    return question('I can provide a weather report. Say location for here, '
                    'a zipcode or tell me a city name and its State')

@ask.intent('AMAZON.PreviousIntent')
@ask.intent('AMAZON.NextIntent')
def misc():
    return question('That does not work with this app. Would you like an'
                    'air status?')


@ask.intent('AMAZON.YesIntent')
def yes():
    return question('Say location for here, '
                    'a zipcode or tell me a city name and its State')

@ask.intent('AMAZON.RepeatIntent')
def repeat():
    repeat_speech = ask_session.attributes['last_speech']
    return question(repeat_speech)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    return question('Sorry I only provide air status. Would you like one?')

