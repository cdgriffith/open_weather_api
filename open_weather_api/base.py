#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Union, Tuple
import gzip
from pathlib import Path

from appdirs import user_data_dir
import requests
import reusables
from box import Box, BoxList

from open_weather_api.exceptions import OpenWeatherAPIError, OpenWeatherError

__all__ = ['OpenWeatherAPI']


@dataclass()
class OpenWeatherAPI:
    """
        Base API for OpenWeather Map to be used with the Free API key from
        https://openweathermap.org
    """

    api_key: str
    api_version: str = '2.5'
    units: str = None
    lang: str = None
    mode: str = None
    city_info: BoxList = None
    city_file_location: Path = Path(user_data_dir('OpenWeatherAPI'), 'city.list.json.gz')

    def api_call(self, endpoint: str, mode: str = None,
                 parse_json: bool = True, pro: bool = False,
                 api_key: str = None, units: str = None, lang: str = None,
                 **parameters):
        """
            Direct call to the OpenWeather API that handles incorporating the
            API key and other parameters then proper handling of the response.
        """
        parameters['APPID'] = api_key or self.api_key
        if units or self.units:
            parameters['units'] = units or self.units
        if lang or self.lang:
            parameters['lang'] = lang or self.lang
        if mode or self.mode:
            # The API does not want a mode being set if requesting the default JSON
            parameters['mode'] = mode or self.mode

        url = f'https://{"pro" if pro else "api"}.openweathermap.org/data/{self.api_version}/{endpoint}'

        result = requests.get(url, params=parameters)

        if result.ok:
            if not mode and not self.mode and parse_json:
                return Box(result.json())
            return result.text

        try:
            message = result.json()["message"]
        except (ValueError, KeyError):
            message = result.text

        del parameters['APPID']
        raise OpenWeatherAPIError(f'Error code {result.status_code} '
                                  f'while calling endpoint "{url}" with parameters {parameters}: {message}')

    def _download_city_list(self):
        if not self.city_file_location.exists():
            self.city_file_location.parent.mkdir(parents=True, exist_ok=True)
            reusables.download('http://bulk.openweathermap.org/sample/city.list.json.gz',
                               filename=str(self.city_file_location))
        return BoxList.from_json(gzip.open(self.city_file_location).read())

    def city_search(self, city_name: str) -> BoxList:
        """Use the downloaded city data to find a city's ID, lat and lon"""
        if not self.city_info:
            try:
                city_info = self._download_city_list()
            except Exception as err:
                print(f'Could not download or transform city information: {err}')
                return BoxList()
            else:
                if not city_info:
                    raise OpenWeatherError('Cannot load city data!')
                self.city_info = city_info
        return BoxList(city for city in self.city_info
                       if city_name.casefold() in city.name.casefold())

    def current_by_city(self, city: str, country: str = 'US', **kwargs) -> Box:
        """Grab current weather data by city name"""
        return self.api_call('weather', q=f'{city},{country}', **kwargs)

    def current_by_zip_code(self, zip_code: Union[int, str], country: str = 'US', **kwargs) -> Box:
        """Grab current weather data by zip code"""
        return self.api_call('weather', zip=f'{zip_code},{country}', **kwargs)

    def current_by_id(self, country_id: Union[int, str], **kwargs) -> Box:
        """Grab current weather data by OpenWeather's city ID"""
        return self.api_call('weather', id=country_id, **kwargs)

    def current_by_lat_lon(self, lat: Union[int, float, str], lon: Union[int, float, str], **kwargs) -> Box:
        """Grab current weather data by latitude and longitude"""
        return self.api_call('weather', lat=lat, lon=lon, **kwargs)

    def current_multiple_by_rect(self, lon_left: Union[int, float, str],
                                 lat_bottom: Union[int, float, str],
                                 lon_right: Union[int, float, str],
                                 lat_top: Union[int, float, str],
                                 zoom: Union[int, str] = 10, **kwargs):
        """Multiple city weather data within a boxed area"""
        return self.api_call('box/city', bbox=f'{lon_left},{lat_bottom},{lon_right},{lat_top},{zoom}', **kwargs)

    def current_multiple_by_cycle(self, lat: Union[int, float, str], lon: Union[int, float, str],
                                  city_count: Union[int, str] = 10, **kwargs) -> Box:
        """Multiple city weather data within a circle from a fixed point"""
        if not isinstance(city_count, int) or city_count > 50 or city_count < 1:
            raise OpenWeatherError('Number of cities requested must be between 1 and 50')
        return self.api_call('find', lat=lat, lon=lon, cnt=city_count, **kwargs)

    def current_multiple_by_id(self, city_ids: Union[List, Tuple, str], **kwargs) -> Box:
        """Multiple city weather data gathered by their OpenWeather city IDs"""
        if isinstance(city_ids, (tuple, list)):
            # The extra safety conversion to str is because the json for city
            # data returns the ids as numbers by default
            city_ids = ','.join((str(x) for x in city_ids))
        return self.api_call('group', id=city_ids, **kwargs)

    def forecast_by_city(self, city: str, country: str = 'US', **kwargs) -> Box:
        """Grab future forecast weather data by city name"""
        return self.api_call('forecast', q=f'{city},{country}', **kwargs)

    def forecast_by_zip_code(self, zip_code: Union[int, str], country: str = 'US', **kwargs) -> Box:
        """Grab future forecast weather data by zip code"""
        return self.api_call('forecast', zip=f'{zip_code},{country}', **kwargs)

    def forecast_by_id(self, country_id: Union[int, str], **kwargs) -> Box:
        """Grab future forecast data by OpenWeather's city ID"""
        return self.api_call('forecast', id=country_id, **kwargs)

    def forecast_by_lat_lon(self, lat: Union[int, float, str], lon: Union[int, float, str], **kwargs) -> Box:
        """Grab future forecast data by latitude and longitude"""
        return self.api_call('forecast', lat=lat, lon=lon, **kwargs)
