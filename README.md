# OpenWeather API 

> This is demo software and should not be used in production

## Installation

OpenWeather API requires at least Python 3.7.

## OpenWeatherAPI 

These methods are available to anyone who has set up a free access token at 
[openweathermap.org](https://openweathermap.org/appid).

Initializing the class `OpenWeatherAPI` takes the following options.

| parameter | default | description |
| --- | --- |  --- | 
| api_key | | **Required** - The token generated on openweathermap.org  |
| api_version | 2.5 | The current (2019-12-14) public api version  |
| units | None (Kelvin) | Temperature in Kelvin is default, also accepts 'metric' or 'imperial'  |
| lang | None (English) | View supported languages [here](https://openweathermap.org/current#multi) |
| mode | None (JSON) | The API can return information in JSON (default), XML or HTML  |
| **Library configuration** | |
| city_info | Empty BoxList | Where the [city data](http://bulk.openweathermap.org/sample/city.list.json.gz) is stored for the class |  
| city_file_location | Path (User storage) | Path to where the city data will be downloaded if required | 

After the class is initialized, the following methods are available. 

| method | parameters |
| --- | --- | 
| **Weather for single region** |  | 
| current_by_city | city_name | 
| current_by_zip_code | zip_code | 
| current_by_id | city_id | 
| current_by_lat_lon | lat, lon | 
| **Weather for multiple regions** | | 
| current_multiple_by_rect | lon_left, lat_bottom, lon_right, lat_top, zoom | 
| current_multiple_by_cycle | lat, lon, city_count | 
| current_multiple_by_id | city_ids | 
| **Forecast for single region** | | 
| forecast_by_city | city_name | 
| forecast_by_zip_code | zip_code | 
| forecast_by_id | city_id | 
| forecast_by_lat_lon | lat, lon | 
| **Additional functions** | |
| api_call | endpoint, **parameters_and_overloads  | 
| city_search | city_name | 

## OpenWeatherPro

This functionality is only available to higher tier price packages, and will return a `401 unauthorized` error if you
do not have the proper plan. 

| method | parameters |
| --- | --- |
| **Hourly forecast**  | | 
| hourly_by_city | city_name |
| hourly_by_zip_code | zip_code |
| hourly_by_id | city_id |
| hourly_by_lat_lon | lat, lon |
| **Two week daily forecast** | |
| two_week_by_city | city_name |
| two_week_by_zip_code | zip_code |
| two_week_by_id | city_id |
| two_week_by_lat_lon | lat, lon |

## Design Rational

### Do you use type hinting all the time?

No. Type hinting is like Christmas music, there is a time for it (after Thanksgiving). As this is a library to be 
used by other programs, with these functions as the interfaces, it is important to make very clear how they should be
used, both in documentation and any IDE help possible. However, for the majority of projects 
I feel that type hinting slows down the development process, makes the code harder to read, and can even take away
from Python's famous duck typing behavior. 

### Why classes?

While I think everyone should watch Jack Diederich's [Stop Writing Classes](https://www.youtube.com/watch?v=5ZKvwuZSiyc)
video, there are cases like this where it makes sense. This library has required initialization information (api key),
reused settings (language, temperature units) and state information (city data), which lends itself well to classes.
On top of that, there is no issue with either storing a single instance or creating a new one each time needed with
how this was designed. 

### What imports are used? 

This API could have easily be written without any non-standard library code. However, the nature of Python is to 
reuse well tested code rather than to rebuild the wheel each time. In this case I am using two of my own libraries, 
[python-box](https://github.com/cdgriffith/Box) and [reusables](https://github.com/cdgriffith/Reusables)
for some helpers, ActiveState's [appdirs](https://github.com/ActiveState/appdirs) to manage cross platform data storage,
and Kenneth Reitz's well known [requests](https://github.com/psf/requests) library 
for talking to the OpenWeather endpoints. 

### Why is lazy loading done for the city data? 

The normal usage of the API does not require the city data, which takes a considerable amount of time to download
and load into memory. It is meant to only be helpful for finding a city's id or location when it cannot be easily 
obtained through a loser name or zip code search. 

### Why can everything be overloaded in `api_call`?

Nearly everything defined at class creation can be overloaded when calling a method for the api call. This is 
in the style of "sensible defaults" but allowing for one off customization. 
