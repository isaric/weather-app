from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from datetime import datetime

date_format_current = "%Y-%m-%dT%H:%M"
date_format_ten_day = "%Y-%m-%d"

def get_plot(weather_data, current):
    if current:
        # Create separate plots for temperature, humidity, and windspeed
        temp_plot = figure(x_axis_type="datetime", title="Temperature (°C)")
        humidity_plot = figure(x_axis_type="datetime", title="Relative Humidity (%)")
        wind_plot = figure(x_axis_type="datetime", title="Wind Speed (km/h)")
        
        time = [datetime.strptime(i, date_format_current) for i in weather_data["hourly"]["time"]]
        
        # Temperature plot
        temp_data = weather_data["hourly"]["temperature_2m"]
        temp_source = ColumnDataSource({'time': time, 'value': temp_data})
        temp_plot.line(x='time', y='value', line_width=2, line_color='red', source=temp_source)
        
        # Humidity plot
        humidity_data = weather_data["hourly"]["relativehumidity_2m"]
        humidity_source = ColumnDataSource({'time': time, 'value': humidity_data})
        humidity_plot.line(x='time', y='value', line_width=2, line_color='green', source=humidity_source)
        
        # Wind speed plot
        wind_data = weather_data["hourly"]["windspeed_10m"]
        wind_source = ColumnDataSource({'time': time, 'value': wind_data})
        wind_plot.line(x='time', y='value', line_width=2, line_color='blue', source=wind_source)
        
        # Generate components for each plot
        temp_script, temp_div = components(temp_plot)
        humidity_script, humidity_div = components(humidity_plot)
        wind_script, wind_div = components(wind_plot)
        
        return {
            'temp_script': temp_script,
            'temp_div': temp_div,
            'humidity_script': humidity_script,
            'humidity_div': humidity_div,
            'wind_script': wind_script,
            'wind_div': wind_div
        }
    else:
        # For 10-day forecast, keep a single plot with max and min temperatures
        plot = figure(x_axis_type="datetime", title="10-day Temperature Forecast")
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
        
        script, div = components(plot)
        return {'script': script, 'div': div}