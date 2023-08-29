from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from datetime import datetime

date_format_current = "%Y-%m-%dT%H:%M"
date_format_ten_day = "%Y-%m-%d"

def get_plot(weather_data, current):
    plot = figure(x_axis_type="datetime")
    
    if current:
        
        y_range = weather_data["hourly"]["temperature_2m"]
        y2 = weather_data["hourly"]["relativehumidity_2m"]
        y3 = weather_data["hourly"]["windspeed_10m"]
        time = [datetime.strptime(i, date_format_current) for i in weather_data["hourly"]["time"]]
        df = {
            'time': [time, time, time], 
            'measure': ['Temp', 'Hum', 'Wind'], 
            'color': ['red', 'green', 'blue'],
            'val': [y_range, y2, y3]
        }
        source = ColumnDataSource(df)
        plot.multi_line(xs='time', ys='val', color='color', legend_field='measure',
             line_width=2, line_alpha=0.6, hover_line_alpha=1.0,
             source=source)
    else:
        time = [datetime.strptime(i, date_format_ten_day) for i in weather_data["daily"]["time"]]
        y_range = weather_data["daily"]["temperature_2m_max"]
        y2 = weather_data["daily"]["temperature_2m_min"]
        df = {
            'time': [time, time], 
            'measure': ['Temp - Max', 'Temp - Min'], 
            'color': ['red', 'green'],
            'val': [y_range, y2]
        }
        source = ColumnDataSource(df)
        plot.multi_line(xs='time', ys='val', color='color', legend_field='measure',
             line_width=2, line_alpha=0.6, hover_line_alpha=1.0, source=source)    
    return components(plot)