
from flask import Flask, render_template, request
import city_search.cities as cities
import open_meteo.client as client
import visualisation.plotter as plotter

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate_report', methods=['POST'])
def generate_report():
    city_name = request.form['city']
    report = request.form['report']
    city = cities.find_city(city_name)
    current = report == "current"
    response = client.get_weather(city["lat"], city["lng"], current)
    script, div = plotter.get_plot(response, current)
    return render_template('report.html', city=city, script=script, div=div)