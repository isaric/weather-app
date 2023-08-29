### weather-app

This is a small demo app that lets the user search for a city from the world list of cities and get
a weather report graph back from the open-metao API.

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


