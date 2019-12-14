#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Union, Tuple

from open_weather_api import OpenWeatherAPI

from box import Box

__all__ = ['OpenWeatherPro']


class OpenWeatherPro(OpenWeatherAPI):

    def hourly_by_city(self, city: str, country: str = 'US', **kwargs) -> Box:
        return self.api_call('forecast/hourly', q=f'{city},{country}', pro=True, **kwargs)

    def hourly_by_zip_code(self, zip_code: Union[int, str], country: str = 'US', **kwargs) -> Box:
        return self.api_call('forecast/hourly', zip=f'{zip_code},{country}', pro=True, **kwargs)

    def hourly_by_id(self, country_id: Union[int, str], **kwargs) -> Box:
        return self.api_call('forecast/hourly', id=country_id, pro=True, **kwargs)

    def hourly_by_lat_lon(self, lat: Union[int, float, str], lon: Union[int, float, str], **kwargs) -> Box:
        return self.api_call('forecast/hourly', lat=lat, lon=lon, pro=True, **kwargs)

    def two_week_by_city(self, city: str, country: str = 'US', **kwargs) -> Box:
        return self.api_call('forecast/daily', q=f'{city},{country}', pro=True, **kwargs)

    def two_week_zip_code(self, zip_code: Union[int, str], country: str = 'US', **kwargs) -> Box:
        return self.api_call('forecast/daily', zip=f'{zip_code},{country}', pro=True, **kwargs)

    def two_week_by_id(self, country_id: Union[int, str], **kwargs) -> Box:
        return self.api_call('forecast/daily', id=country_id, pro=True, **kwargs)

    def two_week_by_lat_lon(self, lat: Union[int, float, str], lon: Union[int, float, str], **kwargs) -> Box:
        return self.api_call('forecast/daily', lat=lat, lon=lon, pro=True, **kwargs)
