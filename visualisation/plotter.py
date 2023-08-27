from bokeh.embed import components
from bokeh.plotting import figure
from datetime import datetime

date_format_current = "%Y-%m-%dT%H:%M"
date_format_ten_day = "%Y-%m-%d"

def get_plot(weather_data, current):
    plot = figure(x_axis_type="datetime")
    if current:
        y_range = weather_data["hourly"]["temperature_2m"]
        y2 = weather_data["hourly"]["relativehumidity_2m"]
        y3 = weather_data["hourly"]["windspeed_10m"]
        x_range = [datetime.strptime(i, date_format_current) for i in weather_data["hourly"]["time"]]
        plot.multi_line([x_range, x_range, x_range], [y_range, y2, y3], color=["red", "green", "blue"], line_width=2)
    else:
        x_range = [datetime.strptime(i, date_format_ten_day) for i in weather_data["daily"]["time"]]
        y_range = weather_data["daily"]["temperature_2m_max"]
        y2 = weather_data["daily"]["temperature_2m_min"]
        plot.multi_line([x_range, x_range], [y_range, y2], color=["red", "green"], line_width=2)
    
    return components(plot)