
from flask import Flask, render_template, request, jsonify
import os
import json
import requests
import city_search.cities as cities
import open_meteo.client as client
import visualisation.plotter as plotter

app = Flask(__name__,
            static_url_path='', 
            static_folder='templates/static',
            template_folder='templates')

def _build_llm_prompt(city: str, weather_data: dict, current: bool) -> str:
    try:
        if current:
            compact = {
                "city": city,
                "type": "current_forecast",
                "current_weather": weather_data.get("current_weather", {}),
                "hourly": {
                    # Limit to first 24 entries to keep prompt compact
                    "time": weather_data.get("hourly", {}).get("time", [])[:24],
                    "temperature_2m": weather_data.get("hourly", {}).get("temperature_2m", [])[:24],
                    "relativehumidity_2m": weather_data.get("hourly", {}).get("relativehumidity_2m", [])[:24],
                    "windspeed_10m": weather_data.get("hourly", {}).get("windspeed_10m", [])[:24],
                },
            }
        else:
            compact = {
                "city": city,
                "type": "ten_day_history",
                "daily": {
                    "time": weather_data.get("daily", {}).get("time", []),
                    "temperature_2m_max": weather_data.get("daily", {}).get("temperature_2m_max", []),
                    "temperature_2m_min": weather_data.get("daily", {}).get("temperature_2m_min", []),
                },
            }
    except Exception:
        compact = {"city": city, "note": "unable to compact weather data"}

    return (
        "You are a helpful weather assistant. Using the provided data, write a concise, friendly description "
        "of the weather and include practical suggestions for clothing and 2-3 suitable activity ideas. "
        "Avoid repeating raw numbers excessively—summarize trends. Keep under 180 words.\n\n"
        f"Weather data (JSON) for {city}:\n" + json.dumps(compact)
    )


def generate_ai_description(city: str, weather_data: dict, current: bool) -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3")
    timeout = float(os.getenv("OLLAMA_TIMEOUT", "10"))

    prompt = _build_llm_prompt(city, weather_data, current)
    try:
        resp = requests.post(
            f"{base_url.rstrip('/')}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        if resp.ok:
            data = resp.json()
            text = data.get("response") or data.get("text") or ""
            if text:
                return text.strip()
        return ""
    except Exception:
        return ""

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

    # Generate AI description (best-effort; ignore failures)
    ai_description = generate_ai_description(city, response, current)
    
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
                              ai_description=ai_description,
                              current=current)
    else:
        # For 10-day forecast, we have a single plot
        return render_template('report.html', 
                              city=city, 
                              title=title,
                              script=plot_components['script'],
                              div=plot_components['div'],
                              ai_description=ai_description,
                              current=current)

@app.route('/autocomplete', methods=['GET'])
def find_cities():
    name = request.args.get('name')
    results = cities.find_city_incomplete(name)
    return jsonify(results)