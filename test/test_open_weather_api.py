from unittest.mock import MagicMock

import pytest

import open_weather_api.base


class FakeRequest:

    def ok(self):
        return True

    def json(self):
        return {}


open_weather_api.base.requests = MagicMock()
open_weather_api.base.requests.get.return_value = FakeRequest()
api_base = 'https://api.openweathermap.org/data/2.5'


class TestOpenWeatherAPI:

    @pytest.fixture(autouse=True)
    def new_instances(self):
        self.api = open_weather_api.base.OpenWeatherAPI('TEST_API_KEY')

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





if __name__ == '__main__':
    pytest.main()
