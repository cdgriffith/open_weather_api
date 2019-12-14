import pytest

from .common import *
from open_weather_api import OpenWeatherPro


api_base = 'https://pro.openweathermap.org/data/2.5'


class TestOpenWeatherAPI:

    @pytest.fixture(autouse=True)
    def new_instances(self):
        self.api = OpenWeatherPro('TEST_API_KEY')

    def test_hourly_city(self):
        self.api.hourly_by_city('London', country='UK')
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/forecast/hourly',
            params={'q': 'London,UK', 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_hourly_id(self):
        self.api.hourly_by_id(2323)
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/forecast/hourly',
            params={'id': 2323, 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_hourly_zip(self):
        self.api.hourly_by_zip_code(15601)
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/forecast/hourly',
            params={'zip': '15601,US', 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_hourly_lat_lon(self):
        self.api.hourly_by_lat_lon(lat=10, lon=20)
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/forecast/hourly',
            params={'lat': 10, 'lon': 20, 'APPID': 'TEST_API_KEY', 'units': 'imperial'})





if __name__ == '__main__':
    pytest.main()
