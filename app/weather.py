# for parsing the weather/pollution report
import requests

weather_status = {'01d': 'It is Sunny', '01n': 'A Clear Night',
                  '02d': 'A few light Clouds', '02n': 'Few Nighttime Clouds',
                  '03d': 'Scattered Clouds', '04d': 'Over cast with Broken Clouds',
                  '09d': 'Rain Showers', '10d': 'Rain', '10n': 'Rain',
                  '11d': 'Thunder Storm', '13d': 'Snow', '50d':'Fog'}

air_status = {'green': 'Good','yellow': 'Moderate',
               'orange': 'Unhealthy for Sensative Groups', 'red': 'unhealthy',
               'purple': 'very unhealthy', 'maroon': 'hazardous'}

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
class GetWeatherData():
    '''Get data from airvisual api, set up properties for needed variables'''
    def __init__(self, city, state):
        self._base_url = 'http://api.airvisual.com/v2/city'
        self.city = city
        self.state = state
        self._params = {'city': city, 'state': state, 'country': 'USA',
                   "key": "YEa4b9c2pNdCTZpNp"}
        self.data = requests.request("GET", self._base_url,
                                     params=self._params).json()


    @property
    def info(self):
        return self.data

    @property
    def aqi(self):
        aqi = (self.data['data']['current']['pollution']['aqius'])
        if aqi <=50:
            air_quality = 'green'
        elif 50 < aqi <= 100:
            air_quality = 'yellow'
        elif 100 < aqi <=150:
            air_quality = 'orange'
        elif 150 < aqi <= 200:
            air_quality = 'red'
        elif 200 < aqi <=300 :
            air_quality = 'purple'
        else:
            air_quality = 'maroon'

        return (str(aqi), air_quality, air_status[air_quality],)

    @property
    def temp(self):
        return str(self.data['data']['current']['weather']['tp'])

    @property
    def humidity(self):
        return str(self.data['data']['current']['weather']['hu'])

    @property
    def wind_speed(self):
        return str(self.data['data']['current']['weather']['ws'])

    @property
    def wind_dir(self):
        ''' wind direction given as degress, converted to cardinal points'''
        wind_dir = self.data['data']['current']['weather']['wd']
        wind_dir = wind_direction(wind_dir)
        return wind_dir

    @property
    def conditions(self):
        conditions = self.data['data']['current']['weather']['ic']
        conditions_text = weather_status[conditions]
        return (conditions, conditions_text)




