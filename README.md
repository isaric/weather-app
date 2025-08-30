### weather-app

This is a small demo app that lets the user search for a city from the world list of cities and get
a weather report graph back from the open-meteo API.

There are two types of data the user can choose from - a prognosis or a the historical data from the
last 10 days. The form offers autocomplete functionality that helps the user choose a city after typing
in the first three letters.

The weather data is visualised using the bokeh library.

The server is built using the Flask Python web framework.

This application was created to help teach learners enrolled in the Python Developer program
at Algebra in Zagreb.

You can also run it as a Docker container. Build your own image using the Dockerfile included in the repo or
pull the public image [here](https://hub.docker.com/r/isaricpv/weather-app)

| Start                                                 | City search                                          |
| ------------------------------------------------------|------------------------------------------------------|
| ![Screen 1](doc/screen_1.png?raw=true "Start")        | ![Screen 2](doc/screen_2.png?raw=true "City Search") |

| Prognosis                                             | Historical                                           |
| ------------------------------------------------------|------------------------------------------------------|
| ![Screen 3](doc/screen_3.png?raw=true "Prognosis")    | ![Screen 4](doc/screen_4.png?raw=true "Historical")  |



## AI Weather Summary (Ollama)

After fetching weather data from Open‑Meteo, the app can optionally call an Ollama LLM to generate a concise weather description with clothing and activity suggestions. The page will still load even if the AI call fails.

Configuration (environment variables):
- OLLAMA_BASE_URL: Base URL of your Ollama instance. Default: http://localhost:11434
- OLLAMA_MODEL: Model name to generate with. Default: llama3
- OLLAMA_TIMEOUT: Request timeout in seconds. Default: 10

Example (Docker):
- Ensure you have an Ollama server running on your host (e.g., listening at http://localhost:11434)
- Run the container and point it at the host Ollama instance:

  docker run -p 5000:5000 \
    -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
    -e OLLAMA_MODEL=llama3 \
    isaricpv/weather-app

Behavior and fallback:
- If the Ollama endpoint is unreachable or returns an error/timeout, the app silently falls back and shows “AI summary is not available right now.”
- The generated description is rendered as plain text (HTML-escaped) inside report.html.
