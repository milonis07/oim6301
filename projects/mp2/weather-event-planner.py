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

    First, I will search for the town using the Open-Meteo geocoding API and find the first matching place in Massachusetts. Then, I will use its latitude and longitude to get the weather forecast for the next seven days. I will collect the high and low temperatures, chance of rain, and strongest wind speed for each day. Next, I will combine these values with their dates and check whether each day meets all the weather rules. If multiple days pass, I will choose the day with the lowest chance of rain, using wind speed to break a tie. If no days pass, I will choose the day that breaks the fewest rules. Finally, I will print a table of the results and a sentence explaining which day is best.

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*

    My loop will carry the weather records for each day, including the date, high and low temperatures, rain probability, and strongest wind speed. It will use these values to check whether each day meets the rules and help determine which day is best.

    - *Which check will you use in section 6, and which two numbers should agree?*

    I will check one day's high temperature by comparing the value returned by my code with the high temperature for the same date in the original API response. The two numbers should agree because they represent the same measurement for the same day.
    """)
    return


if __name__ == "__main__":
    app.run()
