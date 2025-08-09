
from flask import Flask, render_template, request, jsonify
import city_search.cities as cities
import open_meteo.client as client
import visualisation.plotter as plotter

app = Flask(__name__,
            static_url_path='', 
            static_folder='templates/static',
            template_folder='templates')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate_report', methods=['GET'])
def generate_report():
    lat = request.args['lat']
    lng = request.args['lng']
    report = "current"
    if 'report' in request.args:
        report = request.args['report']
    city = request.args['city']
    current = report == "current"
    title = "Forecast" if current else "10-day Historical data"
    response = client.get_weather(lat, lng, current)
    
    plot_components = plotter.get_plot(response, current)
    
    if current:
        # For current weather, we have separate plots for temp, humidity, and wind
        return render_template('report.html', 
                              city=city, 
                              title=title,
                              temp_script=plot_components['temp_script'],
                              temp_div=plot_components['temp_div'],
                              humidity_script=plot_components['humidity_script'],
                              humidity_div=plot_components['humidity_div'],
                              wind_script=plot_components['wind_script'],
                              wind_div=plot_components['wind_div'],
                              current=current)
    else:
        # For 10-day forecast, we have a single plot
        return render_template('report.html', 
                              city=city, 
                              title=title,
                              script=plot_components['script'],
                              div=plot_components['div'],
                              current=current)

@app.route('/autocomplete', methods=['GET'])
def find_cities():
    name = request.args.get('name')
    results = cities.find_city_incomplete(name)
    return jsonify(results)