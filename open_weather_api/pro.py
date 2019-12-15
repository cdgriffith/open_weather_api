#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union

from open_weather_api import OpenWeatherAPI

from box import Box

__all__ = ['OpenWeatherPro']


class OpenWeatherPro(OpenWeatherAPI):
    """
        These API are only available to paid subscribers of higher tier levels at
        https://openweathermap.org. Trying to access them with a standard free
        api key will result in a 401 unauthorized error.
    """

    def hourly_by_city(self, city: str, country: str = 'US', **kwargs) -> Box:
        """Grab four days worth of hourly forecast info by city name"""
        return self.api_call('forecast/hourly', q=f'{city},{country}', pro=True, **kwargs)

    def hourly_by_zip_code(self, zip_code: Union[int, str], country: str = 'US', **kwargs) -> Box:
        """Grab four days worth of hourly forecast info by zip code"""
        return self.api_call('forecast/hourly', zip=f'{zip_code},{country}', pro=True, **kwargs)

    def hourly_by_id(self, country_id: Union[int, str], **kwargs) -> Box:
        """Grab four days worth of hourly forecast info by city id"""
        return self.api_call('forecast/hourly', id=country_id, pro=True, **kwargs)

    def hourly_by_lat_lon(self, lat: Union[int, float, str], lon: Union[int, float, str], **kwargs) -> Box:
        """Grab four days worth of hourly forecast info by lat and lon"""
        return self.api_call('forecast/hourly', lat=lat, lon=lon, pro=True, **kwargs)

    def two_week_by_city(self, city: str, country: str = 'US', **kwargs) -> Box:
        """16 days worth of forecast data in 3 hour segments by city name"""
        return self.api_call('forecast/daily', q=f'{city},{country}', pro=True, **kwargs)

    def two_week_by_zip_code(self, zip_code: Union[int, str], country: str = 'US', **kwargs) -> Box:
        """16 days worth of forecast data in 3 hour segments by zip code"""
        return self.api_call('forecast/daily', zip=f'{zip_code},{country}', pro=True, **kwargs)

    def two_week_by_id(self, country_id: Union[int, str], **kwargs) -> Box:
        """16 days worth of forecast data in 3 hour segments by city id"""
        return self.api_call('forecast/daily', id=country_id, pro=True, **kwargs)

    def two_week_by_lat_lon(self, lat: Union[int, float, str], lon: Union[int, float, str], **kwargs) -> Box:
        """16 days worth of forecast data in 3 hour segments by lat and lon"""
        return self.api_call('forecast/daily', lat=lat, lon=lon, pro=True, **kwargs)
