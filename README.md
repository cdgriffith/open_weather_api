# OpenWeather API 

> This is demo software and should not be used in production

## OpenWeatherAPI 

| method | parameters | description |
| --- | --- | --- |
| **Weather for single region** |  |  |  
| current_by_city | city_name | |
| current_by_zip_code | zip_code | |
| current_by_id | city_id | |
| current_by_lat_lon | lat, lon | |
| **Weather for multiple regions** | | | 
| current_multiple_by_rect | lon_left, lat_bottom, lon_right, lat_top, zoom | |
| current_multiple_by_cycle | lat, lon, cities | |
| current_multiple_by_id | city_ids | |
| **Forecast for single region** | | | 
| forecast_by_city | city_name | |
| forecast_by_zip_code | zip_code | |
| forecast_by_id | city_id | |
| forecast_by_lat_lon | lat, lon | |

## OpenWeatherPro

| method | parameters | description |
| --- | --- | --- |
| **Hourly forecast**  | | | 
| hourly_by_city | city_name | |
| hourly_by_zip_code | zip_code | |
| hourly_by_id | city_id | |
| hourly_by_lat_lon | lat, lon | |
| **Two week daily forecast** | | |
| two_week_by_city | city_name | |
| two_week_by_zip_code | zip_code | |
| two_week_by_id | city_id | |
| two_week_by_lat_lon | lat, lon | |

## Design considerations

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