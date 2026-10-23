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
    return (
        highest_high_f,
        lowest_high_f,
        max_rain_chance,
        max_wind_mph,
        place,
        state,
    )


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(location):
    print(f"Location selected: {location['name']}, {location['admin1']}")
    return


@app.cell
def _(
    forecast_records,
    highest_high_f,
    lowest_high_f,
    max_rain_chance,
    max_wind_mph,
):
    passing_days = []
    evaluated_days = []

    for _day in forecast_records:
        _passes_temperature = (
            _day["high_f"] >= lowest_high_f
            and _day["high_f"] <= highest_high_f
        )
        _passes_rain = _day["rain_chance"] <= max_rain_chance
        _passes_wind = _day["wind_mph"] <= max_wind_mph

        _passes_all = (
            _passes_temperature and _passes_rain and _passes_wind
        )

        _rules_broken = 0
        if not _passes_temperature:
            _rules_broken = _rules_broken + 1
        if not _passes_rain:
            _rules_broken = _rules_broken + 1
        if not _passes_wind:
            _rules_broken = _rules_broken + 1

        _day_result = {
            "date": _day["date"],
            "high_f": _day["high_f"],
            "low_f": _day["low_f"],
            "rain_chance": _day["rain_chance"],
            "wind_mph": _day["wind_mph"],
            "passes": _passes_all,
            "rules_broken": _rules_broken
        }

        evaluated_days.append(_day_result)

        if _passes_all:
            passing_days.append(_day_result)

    print("Number of evaluated days:", len(evaluated_days))
    return evaluated_days, passing_days


@app.cell
def _(evaluated_days, passing_days):
    if len(passing_days) > 0:
        best_day = passing_days[0]

        for _day in passing_days:
            if _day["rain_chance"] < best_day["rain_chance"]:
                best_day = _day
            elif (
                _day["rain_chance"] == best_day["rain_chance"]
                and _day["wind_mph"] < best_day["wind_mph"]
            ):
                best_day = _day

        recommendation_reason = "lowest chance of rain among passing days"
    else:
        best_day = evaluated_days[0]

        for _day in evaluated_days:
            if _day["rules_broken"] < best_day["rules_broken"]:
                best_day = _day

        recommendation_reason = (
            "breaks the fewest weather rules; no day passes every rule"
        )
    return (best_day,)


@app.cell
def _(evaluated_days):
    print(
        f"{'Date':<12}"
        f"{'High (°F)':>11}"
        f"{'Low (°F)':>11}"
        f"{'Rain (%)':>11}"
        f"{'Wind (mph)':>12}"
        f"{'Passes?':>10}"
    )
    print("-" * 67)

    for _day in evaluated_days:
        print(
            f"{_day['date']:<12}"
            f"{_day['high_f']:>11.1f}"
            f"{_day['low_f']:>11.1f}"
            f"{_day['rain_chance']:>11}"
            f"{_day['wind_mph']:>12.1f}"
            f"{str(_day['passes']):>10}"
        )
    return


@app.cell
def _(best_day):
    if best_day is not None:
        print(
            f"The best day for your outdoor event is {best_day['date']} "
            f"with a high of {best_day['high_f']}°F, "
            f"a low of {best_day['low_f']}°F, "
            f"{best_day['rain_chance']}% chance of rain, "
            f"and maximum wind speed of {best_day['wind_mph']} mph."
        )
    else:
        print("No recommendation could be made because no forecast days were available.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(best_day):
    check_date = best_day["date"]
    code_high = best_day["high_f"]

    print("Recommended date checked:", check_date)
    print("High temperature from code:", code_high)
    return check_date, code_high


@app.cell
def _(check_date, code_high, location, requests):
    api_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
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
    )

    api_response.raise_for_status()
    api_daily = api_response.json()["daily"]

    api_high_live = None

    for _date, _high in zip(api_daily["time"], api_daily["temperature_2m_max"]):
        if _date == check_date:
            api_high_live = _high

    print("High temperature from code:", code_high)
    print("High temperature from live API:", api_high_live)
    print("Temperatures agree:", code_high == api_high_live)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    While building the evaluation step in Section 5, I noticed evaluated_days showed 28 records instead of 7. I checked len(forecast_records) first, which correctly showed 7, so the extra records weren't coming from the API — they were coming from my own notebook. I found that the evaluation loop had been wrapped inside def _():, which hid evaluated_days and passing_days as local variables that never reached the rest of the notebook, while a leftover duplicate version of the same loop was still running elsewhere and adding to the same list four times. I removed the def _(): wrapper so the loop ran as plain top-level code, deleted the duplicate, and re-ran the notebook. After that, len(forecast_records) and len(evaluated_days) both showed 7, and the printed table showed each day exactly once, which told me the fix worked.

    Cell reference: Cell 15 in Section 5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading it Back

    *Pick two functions in your notebook that your agent wrote or helped write. For each, write in your own words what goes in, what comes out, and one line you had to ask about. Then choose one change to what the tool does, such as another county, another week or another rule.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first function, `get_location(place, state)`, takes a town name and state, like Wellesley and Massachusetts, and returns the matching location information, including its latitude and longitude. I had to understand how the line `if _result.get("admin1") == state:` works. I learned that it checks whether the location belongs to the state I entered, so the function selects a matching town rather than a town with the same name in another state.

    The second function, `get_forecast(latitude, longitude)`, takes a location’s latitude and longitude and returns a list of daily weather records for the next seven days. Each record includes the date, high and low temperatures, chance of rain, and maximum wind speed. I had to understand the line `return forecast_records`. I learned that it sends the completed list of daily weather records back to the rest of the program, so the weather rules can evaluate each day and recommend the best one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Prediction:** I will change `place` from `"Wellesley"` to `"Lexington"` while keeping the other inputs the same. I expect the tool to retrieve Lexington's location and use its latitude and longitude to fetch a new seven-day weather forecast. Since the weather conditions may differ between the two towns, I expect the table and recommended day to potentially change. The temperature, rain, and wind limits will remain the same.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Result:** I changed the location from Wellesley to Lexington and reran the notebook. The forecast and recommendation updated, and the recommended day's high temperature matched the original API response. The verification returned `True`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(location, passing_days, requests):
    # Going Further: Compare daylight hours on suitable event days

    daylight_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "daily": "sunrise,sunset",
            "timezone": "America/New_York",
            "forecast_days": 7
        }
    )

    daylight_response.raise_for_status()
    daylight_data = daylight_response.json()["daily"]

    daylight_by_date = {}

    for _date, _sunrise, _sunset in zip(
        daylight_data["time"],
        daylight_data["sunrise"],
        daylight_data["sunset"]
    ):
        daylight_by_date[_date] = {
            "sunrise": _sunrise,
            "sunset": _sunset
        }

    print("Daylight information for passing days:")

    for _day in passing_days:
        _daylight = daylight_by_date.get(_day["date"])

        if _daylight is not None:
            print(
                f"{_day['date']}: "
                f"Sunrise {_daylight['sunrise']}, "
                f"Sunset {_daylight['sunset']}"
            )
    return (daylight_by_date,)


@app.cell
def _(daylight_by_date, passing_days):
    # Going Further: Calculate daylight hours for suitable days

    print("Daylight duration on passing days:")

    for _day in passing_days:
        _daylight = daylight_by_date.get(_day["date"])

        if _daylight is not None:
            _sunrise = _daylight["sunrise"]
            _sunset = _daylight["sunset"]

            _sunrise_minutes = int(_sunrise[11:13]) * 60 + int(_sunrise[14:16])
            _sunset_minutes = int(_sunset[11:13]) * 60 + int(_sunset[14:16])

            _daylight_hours = (_sunset_minutes - _sunrise_minutes) / 60

            print(
                f"{_day['date']}: "
                f"{_daylight_hours:.2f} hours of daylight"
            )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What I tried for going further:

    I extended my weather planner by retrieving sunrise and sunset times from Open-Meteo. I combined this information with the days that passed my original weather rules to see how much daylight would be available for an outdoor event. This extension is included in the Section 9 cell.

    I extended my tool to calculate the number of daylight hours for each day that passes the weather rules. This makes it easier to compare suitable event days based on both weather conditions and available daylight. The calculation is included in the additional Section 9 cell.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent:

    5 hours
    """)
    return


if __name__ == "__main__":
    app.run()
