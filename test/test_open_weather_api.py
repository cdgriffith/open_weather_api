import pytest
from box import BoxList

from .common import *

api_base = 'https://api.openweathermap.org/data/2.5'

cities = BoxList([{"id": 727762, "name": "Rastnik", "country": "BG", "coord": {"lon": 25.283331, "lat": 41.400002}},
                  {"id": 2613357, "name": "Smidstrup", "country": "DK", "coord": {"lon": 12.55787, "lat": 55.865688}}])


class TestOpenWeatherAPI:

    @pytest.fixture(autouse=True)
    def new_instances(self):
        self.api = open_weather_api.base.OpenWeatherAPI('TEST_API_KEY',
                                                        city_ids=cities)

    def test_current_city(self):
        self.api.current_by_city('London', country='UK')
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/weather',
            params={'q': 'London,UK', 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_current_id(self):
        self.api.current_by_id(2323)
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/weather',
            params={'id': 2323, 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_current_zip(self):
        self.api.current_by_zip_code(15601)
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/weather',
            params={'zip': '15601,US', 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_current_lat_lon(self):
        self.api.current_by_lat_lon(lat=10, lon=20)
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/weather',
            params={'lat': 10, 'lon': 20, 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_search(self):
        result = self.api.city_search('rast')
        assert result[0].id == 727762

    def test_multiple_rect(self):
        self.api.current_multiple_by_rect(5, 10, 15, 20, 10)
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/box/city',
            params={'bbox': '5,10,15,20,10', 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_multiple_id(self):
        self.api.current_multiple_by_id([1, 2])
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/group',
            params={'id': '1,2', 'APPID': 'TEST_API_KEY', 'units': 'imperial'})

    def test_multiple_circle(self):
        self.api.current_multiple_by_cycle(1,2,10)
        open_weather_api.base.requests.get.assert_called_with(
            f'{api_base}/find',
            params={'lat': 1, 'lon': 2, 'cnt': 10, 'APPID': 'TEST_API_KEY', 'units': 'imperial'})