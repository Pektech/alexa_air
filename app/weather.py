# for parsing the weather/pollution report

weather_status = {'01d': 'It is Sunny', '01n': 'A Clear Night',
                  '02d': 'A few light Clouds', '02n': 'Few Nighttime Clouds',
                  '03d': 'Scattered Clouds', '04d': 'Over cast with Broken Clouds',
                  '09d': 'Rain Showers', '10d': 'Rain', '10n': 'Rain',
                  '11d': 'Thunder Storm', '13d': 'Snow', '50d':'Fog'}

def wind_direction(wind):
    '''convert wind angle into compass points
    thanks to https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f &
    https://github.com/rezemika/goose-search/blob/master/search/utils.py'''

    dirs = ["North", "North East", "East", "South East", "South",
            "South West", "West", "North West"]
    ix = int((wind + 22.5) / 45)
    return dirs[ix % 8]



def parse_weather(response):
    aqius = str(response['data']['current']['pollution']['aqius'])
    temp = str(response['data']['current']['weather']['tp'])
    humidity = str(response['data']['current']['weather']['hu'])
    wind_speed = str(response['data']['current']['weather']['ws'])
    wind = response['data']['current']['weather']['wd']
    conditions = response['data']['current']['weather']['ic']
    conditions = weather_status[conditions]
    wind = wind_direction(wind)
    return {'aqius': aqius, 'temp': temp, 'humidity': humidity,
            'wind_speed': wind_speed, 'wind': wind, 'conditions': conditions
            }