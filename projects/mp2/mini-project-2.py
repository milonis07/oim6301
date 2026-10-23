import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


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


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
