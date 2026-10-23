import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import requests

    return (requests,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*

    This tool is for a student club organizer who needs to choose the best day for an outdoor event in Massachusetts. It checks the weather forecast for the next seven days and recommends a day based on temperature, rain probability, and wind speed so the event can be planned for a day with suitable weather.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    ### My Plan Before AI

    First, I will search for the town entered by the user using the Open-Meteo geocoding API. I will select the first result that matches the requested state and use its latitude and longitude to find the weather forecast. Next, I will request the daily forecast for the next seven days, including today, with temperatures in Fahrenheit and wind speed in miles per hour. I will combine each date with its high temperature, low temperature, chance of rain, and maximum wind speed into one record. Then, I will check each day against the temperature, rain, and wind limits entered by the user. If multiple days meet all the rules, I will select the day with the lowest chance of rain, using lower wind speed to break a tie. If no day meets all the rules, I will select the day that breaks the fewest rules. Finally, I will print a table comparing the seven days and a sentence recommending the best day.

    **Which functions will your tool need? For each, what goes in and what comes out?**

    I will need a `get_location(place, state)` function that takes the town and state as inputs and returns the first matching location record, including its latitude and longitude. I will also need a `get_forecast(latitude, longitude)` function that takes the coordinates as inputs, requests the weather forecast, and returns a list of daily weather records containing each date, high and low temperatures, rain probability, and maximum wind speed.

    **Which addresses will they request?**

    The location function will request `https://geocoding-api.open-meteo.com/v1/search` to find the town. The forecast function will request `https://api.open-meteo.com/v1/forecast` using the selected location's coordinates and the daily weather fields, Fahrenheit temperatures, miles-per-hour wind speeds, the local time zone, and seven forecast days.

    **How will you know you have every record?**

    I will check that the forecast contains seven dates and that each daily weather field contains seven values. I will combine the dates and weather values in order using `zip()`, then check that the resulting list contains seven daily records.


    **Which check will you use in Section 6, and which two numbers should agree?**

    I will verify the high temperature for one selected date by comparing the high temperature in my code's daily record with the high temperature for the same date in the original Open-Meteo API response. The two numbers should agree because they represent the same day's forecast.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.
    """)
    return


@app.cell
def _():
    place = "Wellesley"
    state = "Massachusetts"
    lowest_high_f = 55
    highest_high_f = 80
    max_rain_chance = 30
    max_wind_mph = 15
    return place, state


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(requests):
    def get_location(place, state):
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": place,
            "count": 100,
            "language": "en",
            "format": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for _result in data.get("results", []):
            if _result.get("admin1") == state:
                return _result

        return None


    return (get_location,)


@app.cell
def _(get_location, place, state):
    location = get_location(place, state)
    print(location)
    return (location,)


@app.cell
def _(requests):
    def get_forecast(latitude, longitude):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": (
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max,"
                "wind_speed_10m_max"
            ),
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
            "forecast_days": 7
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        daily = data["daily"]

        forecast_records = []

        for _date, _high, _low, _rain, _wind in zip(
            daily["time"],
            daily["temperature_2m_max"],
            daily["temperature_2m_min"],
            daily["precipitation_probability_max"],
            daily["wind_speed_10m_max"]
        ):
            _record = {
                "date": _date,
                "high_f": _high,
                "low_f": _low,
                "rain_chance": _rain,
                "wind_mph": _wind
            }
            forecast_records.append(_record)

        return forecast_records


    return (get_forecast,)


@app.cell
def _(get_forecast, location):
    forecast_records = get_forecast(
        location["latitude"],
        location["longitude"]
    )

    print(forecast_records)
    print("Number of forecast records:", len(forecast_records))
    return (forecast_records,)


@app.cell
def _(forecast_records):
    print("Number of dates:", len(forecast_records))
    print("All seven days retrieved:", len(forecast_records) == 7)
    return


@app.cell
def _(forecast_records):
    import json
    from pathlib import Path

    data_directory = Path("projects/mp2/data")
    data_directory.mkdir(parents=True, exist_ok=True)

    data_file = data_directory / "weather_forecast.json"

    with data_file.open("w", encoding="utf-8") as _file:
        json.dump(forecast_records, _file, indent=2)

    print("Records saved:", len(forecast_records))
    print("File exists:", data_file.exists())
    print("Saved to:", data_file)

    return


if __name__ == "__main__":
    app.run()
