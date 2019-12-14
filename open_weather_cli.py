#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from pathlib import Path
from argparse import ArgumentParser

from box import Box
from reusables import win_based

from open_weather_api import OpenWeatherAPI

token_file = Path('.open_weather_token')


def get_owa_class(units=None):
    token = token_file.read_text().strip() if token_file.exists() else None
    if not token:
        token = input('Please enter token (or save to ".open_weather_token" and rerun): ')
    return OpenWeatherAPI(token, units=units)


def forecast(zip_code, country, units=None):
    owa = get_owa_class(units)
    cast = owa.forecast_by_zip_code(zip_code, country=country)

    print(f"{cast.city.name}, {cast.city.country}\t\t\t\t"
          f"sunrise {datetime.fromtimestamp(cast.city.sunrise).strftime('%I:%M%p')} | "
          f"sunset {datetime.fromtimestamp(cast.city.sunset).strftime('%I:%M%p')} ")

    unit_type = 'K'
    if units:
        unit_type = 'C' if units.lower() == 'celsius' else 'F'

    last_date = datetime.fromtimestamp(cast.list[0].dt).strftime('%Y-%m-%d')
    current_row = f"{last_date} | {{padding}}"
    for item in cast.list:
        dt_object = datetime.fromtimestamp(item.dt)
        day = dt_object.strftime('%Y-%m-%d')
        if day != last_date:
            last_date = day
            print(current_row.format(padding=" " * (133 - len(current_row))))
            current_row = f"{day} |"
        current_row = f"{current_row} {dt_object.strftime('%#I%p'):>4} {int(item.main.temp):>4d}°{unit_type} |"
    print(current_row)


def main():
    parser = ArgumentParser('forecast')
    parser.add_argument('--units', help='Temperature unit type, defaults to Kelvin, '
                                        'can also use "imperial" or "celsius" ')
    parser.add_argument('--country', default='US',
                        help='Country for zip code, defaults to "US"')
    parser.add_argument('zip', nargs=1, help='zip code')

    args = parser.parse_args(namespace=Box())
    units = None
    if args.units:
        if args.units.lower() in ('imperial', 'celsius'):
            units = args.units.lower()
        elif args.units.lower() == 'f':
            units = 'imperial'
        elif args.units.lower() == 'c':
            units = 'celsius'
    forecast(args.zip[0], country=args.country, units=units)


if __name__ == '__main__':
    main()
