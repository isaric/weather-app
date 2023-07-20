import requests
import datetime

url = "https://api.open-meteo.com/v1/forecast"
date_format = "%Y-%m-%d"

def get_weather(lat,long,current):
    start_date = datetime.date.today() - datetime.timedelta(days=10)
    end_date = datetime.date.today()
    additional_params = {}
    if current:
        additional_params = {"hourly" : "temperature_2m,relativehumidity_2m,windspeed_10m", "current_weather" : "true"}
    else:
        additional_params = {"daily" : "temperature_2m_max,temperature_2m_min", "timezone" : "auto", "start_date" : datetime.date.strftime(start_date, date_format), "end_date" : datetime.date.strftime(end_date, date_format) }

    params = {"latitude" : lat, "longitude" : long}
    params.update(additional_params)
    response = requests.get(url, params=params)
    return response.json()