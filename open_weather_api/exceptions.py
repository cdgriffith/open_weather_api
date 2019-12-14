#!/usr/bin/env python
# -*- coding: utf-8 -*-


class OpenWeatherError(Exception):
    """An error occurred in the OpenWeatherWrapper library"""


class OpenWeatherAPIError(OpenWeatherError):
    """An unexpected api condition was reached"""
