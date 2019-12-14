#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Union, Tuple
import os
import gzip

import requests
import reusables
from box import Box, BoxList

from open_weather_wrapper.exceptions import OpenWeatherAPIError, OpenWeatherError


@dataclass()
class OpenWeatherAPI:

    api_key: str
    api_version: str = '2.5'
    units: str = 'imperial'
    city_ids: BoxList = None
    lang: str = None

    def api_call(self, endpoint: str, mode: str = 'json',
                 parse_json: bool = True, pro: bool = False, **parameters):
        parameters['APPID'] = self.api_key
        parameters['units'] = self.units
        if self.lang:
            parameters['lang'] = self.lang
        if mode != 'json':
            # The API does not want a mode being set if requesting the default JSON
            parameters['mode'] = mode

        url = f'https://{"pro" if pro else "api"}.openweathermap.org/data/{self.api_version}/{endpoint}'

        result = requests.get(url, params=parameters)

        if result.ok:
            if mode == 'json' and parse_json:
                return Box(result.json())
            return result.text

        try:
            message = result.json()["message"]
        except ValueError:
            message = result.text

        raise OpenWeatherAPIError(f'Error code {result.status_code} '
                                  f'while calling endpoint "{url}": {message}')

    def _download_city_list(self):
        if not os.path.exists('city.list.json.gz'):
            reusables.download('http://bulk.openweathermap.org/sample/city.list.json.gz',
                               filename='city.list.json.gz')
        self.city_ids = BoxList.from_json(gzip.open('city.list.json.gz').read())

    def current_by_city(self, city: str, country: str = 'us', **kwargs) -> Box:
        return self.api_call('weather', q=f'{city},{country}', **kwargs)

    def current_by_zip_code(self, zip_code: Union[int, str], country: str = 'US', **kwargs) -> Box:
        return self.api_call('weather', zip=f'{zip_code},{country}', **kwargs)

    def current_by_id(self, country_id: Union[int, str], **kwargs) -> Box:
        return self.api_call('weather', id=country_id, **kwargs)

    def current_by_lat_lon(self, lat: Union[int, float, str], lon: Union[int, float, str], **kwargs) -> Box:
        return self.api_call('weather', lat=lat, lon=lon, **kwargs)

    def current_multiple_by_rect(self, lon_left: Union[int, float, str],
                                 lat_bottom: Union[int, float, str],
                                 lon_right: Union[int, float, str],
                                 lat_top: Union[int, float, str],
                                 zoom: Union[int, str] = 10, **kwargs):
        return self.api_call('box/city', bbox=f'{lon_left},{lat_bottom},{lon_right},{lat_top},{zoom}', **kwargs)

    def current_multiple_by_cycle(self, lat: Union[int, float, str], lon: Union[int, float, str],
                                  cities: Union[int, str] = 10, **kwargs) -> Box:
        if not isinstance(cities, int) or 1 < cities > 50:
            raise OpenWeatherError('Number of cities requested must be between 1 and 50')
        return self.api_call('find', lat=lat, lon=lon, cnt=cities, **kwargs)

    def current_multiple_by_id(self, city_ids: Union[List, Tuple, str], **kwargs) -> Box:
        if isinstance(city_ids, (tuple, list)):
            # The extra safety conversion to str is because the json for city
            # data returns the ids as numbers by default
            city_ids = ','.join((str(x) for x in city_ids))
        return self.api_call('group', id=city_ids, **kwargs)

    def city_id_search(self, city_name: str) -> BoxList:
        if not self.city_ids:
            self._download_city_list()
        return BoxList(city for city in self.city_ids if city_name.casefold() in city.name.casefold())

