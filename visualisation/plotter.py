from bokeh.embed import components
from bokeh.plotting import figure

def get_plot(weather_data, current):
    plot = figure(x_axis_type="datetime")
    if current:
        y_range = weather_data["hourly"]["temperature_2m"]
        y2 = weather_data["hourly"]["relativehumidity_2m"]
        y3 = weather_data["hourly"]["windspeed_10m"]
        x_range = [i for i in range(1,len(weather_data["hourly"]["temperature_2m"]))]
        plot.multi_line([x_range, x_range, x_range], [y_range, y2, y3], color=["red", "green", "blue"], line_width=2)
    else:
        x_range = [i for i in range(1,len(weather_data["daily"]["temperature_2m_max"]))]
        y_range = weather_data["daily"]["temperature_2m_max"]
        y2 = weather_data["daily"]["temperature_2m_min"]
        plot.multi_line([x_range, x_range], [y_range, y2], color=["red", "green"], line_width=2)
    
    return components(plot)