#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass

import requests

from open_weather_wrapper.exceptions import OpenWeatherAPIError


@dataclass()
class OpenWeatherAPI:

    api_key: str
    base_url: str = 'https://api.openweathermap.org/data'
    api_version: str = '2.5'

    def api_call(self, endpoint: str, mode: str = 'json', parse_json: bool = True, **parameters):
        parameters['APPID'] = self.api_key
        if mode != 'json':
            # The API does not want a mode being set if requesting the default JSON
            parameters['mode'] = mode

        result = requests.get(f'{self.base_url}/{self.api_version}/{endpoint}', params=parameters)

        if result.ok:
            if mode == 'json' and parse_json:
                return result.json()
            return result.text
        raise OpenWeatherAPIError(f'Error code {result.status_code} '
                                  f'while calling endpoint "{endpoint}": {result.text}')

