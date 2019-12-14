#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
from argparse import ArgumentParser

from box import Box

from open_weather_api import OpenWeatherAPI


def get_owa_class(token_file, units=None):
    """
        Helper function to create the OpenWeatherAPI class, making sure to
        find the api token to use beforehand.
    """
    token_file = Path(token_file)
    token = token_file.read_text().strip() if token_file.exists() else None
    if not token:
        print(f'Could not read token file "{token_file}"')
        token = input('Please enter token: ')
    return OpenWeatherAPI(token, units=units)


def current(data, unit_type):
    """View the current weather data for a location"""
    speed_measure = "mph" if unit_type == "F" else "㎧"
    print(f'{data.name}, {data.sys.country}')
    print(f'Condition:   {data.weather[0].main}')
    print(f'Temperature: {data.main.temp}°{unit_type}')
    print(f'Feels like:  {data.main.feels_like}°{unit_type}')
    print(f'Humidity:    {data.main.humidity}%')
    print(f'Wind:        {data.wind.speed}{speed_measure}')
    print(f'Sunrise:     {datetime.fromtimestamp(data.sys.sunrise).strftime("%I:%M%p")}')
    print(f'Sunset:      {datetime.fromtimestamp(data.sys.sunset).strftime("%I:%M%p")}')


def future(data, unit_type):
    """View the future temperatures of a location"""
    print(f'{data.city.name}, {data.city.country}')

    last_date = datetime.fromtimestamp(data.list[0].dt).strftime('%Y-%m-%d')
    print("           |      12AM      |      3AM       |      6AM       |      9AM       |"
          "     Noon       |      3PM       |      6PM       |      9PM       |")
    current_row = f'{last_date} | {{padding}}'
    for item in data.list:
        dt_object = datetime.fromtimestamp(item.dt)
        day = dt_object.strftime('%Y-%m-%d')
        if day != last_date:
            last_date = day
            print(current_row.format(padding=' ' * (157 - len(current_row))))
            current_row = f'{day} |'
        current_row = f'{current_row} {int(item.main.temp):>4d}°{unit_type}{item.weather[0].main:>8} |'
    print(current_row)


def get_units(args):
    units = None
    if args.units:
        if args.units.lower() in ('imperial', 'celsius'):
            units = args.units.lower()
        elif args.units.lower() == 'f':
            units = 'imperial'
        elif args.units.lower() == 'c':
            units = 'celsius'
    unit_type = 'K'
    if units:
        unit_type = 'C' if units.lower() == 'celsius' else 'F'

    return units, unit_type


def main():
    parser = ArgumentParser('forecast')
    parser.add_argument('--units', help='Temperature unit type, defaults to Kelvin, '
                                        'can also use "imperial" or "celsius" ')
    parser.add_argument('--country', default='US',
                        help='Country for zip code, defaults to "US"')
    parser.add_argument('--token-file', default='.open_weather_token',
                        help='File containing the OpenWeather API token')
    parser.add_argument('zip', nargs=1, help='zip code')
    parser.add_argument('--current', help='View current weather conditions',
                        action='store_true')

    args = parser.parse_args(namespace=Box())
    units, unit_type = get_units(args)

    owa = get_owa_class(args.token_file, units)

    try:
        if args.current:
            return current(owa.current_by_zip_code(args.zip[0], country=args.country), unit_type)
        return future(owa.forecast_by_zip_code(args.zip[0], country=args.country), unit_type)
    except KeyError:
        print("Warning: That location did not include all expect output, please try another zip, like 15601")


if __name__ == '__main__':
    main()
