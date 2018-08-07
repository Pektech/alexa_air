# for parsing the weather/pollution report
import requests
from geopy.geocoders import Nominatim

weather_status = {'01d': 'sunny', '01n': 'a clear night',
                  '02d': 'a few light clouds', '02n': 'a few nighttime clouds',
                  '03d': 'scattered clouds', '04d': 'over cast with broken clouds',
                  '09d': 'rain showers', '10d': 'rain', '10n': 'rain',
                  '11d': 'thunder storms', '13d': 'snow', '50d':'fog'}

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



def get_coordinates(location):
    geolocator = Nominatim(user_agent='alexa_air')
    coordinates = geolocator.geocode(location)
    return (coordinates.latitude, coordinates.longitude)


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
        temp = self.data['data']['current']['weather']['tp']
        temp = 9.0/5.0 * temp +32
        return str(round(temp))

    @property
    def humidity(self):
        return str(self.data['data']['current']['weather']['hu'])

    @property
    def wind_speed(self):
        return str(self.data['data']['current']['weather']['ws'])

    @property
    def wind_dir(self):
        ''' wind direction given as degrees, converted to cardinal points'''
        wind_dir = self.data['data']['current']['weather']['wd']
        wind_dir = wind_direction(wind_dir)
        return wind_dir

    @property
    def conditions(self):
        conditions = self.data['data']['current']['weather']['ic']
        conditions_text = weather_status[conditions]
        return conditions, conditions_text



    @property
    def status(self):
        status = self.data['status']
        if status == 'error' or status == 'fail':
            status = (self.data['status'], self.data['data']['message'])
            return status
        else:
            return (status, 'ok')


class GetZipWeather(GetWeatherData):
    '''subclass for zipcodes'''
    def __init__(self, zipcode):
        super().__init__(city=None, state=None)
        self.zipcode = zipcode
        self._base_url = 'http://api.airvisual.com/v2/nearest_city'
        coordinates = get_coordinates(self.zipcode)
        self._params = {'lat': coordinates[0], 'lon': coordinates[1],
                        "key": "YEa4b9c2pNdCTZpNp"}
        self.data = requests.request("GET", self._base_url,
                                     params=self._params).json()