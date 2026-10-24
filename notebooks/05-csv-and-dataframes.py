# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "altair",
#     "polars",
#     "requests",
# ]
# ///
"""From a CSV file to a dataframe.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import csv

    import altair as alt
    import polars as pl
    import requests

    return alt, csv, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # From a CSV File to a Dataframe

    In this notebook you save the towns you read from the course API last week to a file, read them back, and answer one question about them three ways: with a loop, in polars and in SQL. Then you chart the answer.

    | | |
    |---|---|
    | ✏️ | Your turn. Add cells with the **+** button |
    | 🚀 | This week's work |

    For a written answer, add a cell under the question, open the cell's **⋯** menu and choose **Convert to Markdown**.

    Every ✏️ is part of this week's work. The **Going further** at the end of an exercise is optional; try it once the rest is done.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Work with your agent the same way as in notebook 4.** Try it yourself first, or write the steps in words. Then ask your agent, ask it to explain any line you could not have written, and ask which concepts its answer used. Exercise A is by hand.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 1. Saving What You Fetched

    The towns you read last week lived in memory, and they were gone when the notebook stopped. An API also changes. The shop takes new orders every day, and the tax figures change every year. **Save a copy to a file**, and the same analysis runs again on the same data, without a network, and anybody can open it in a spreadsheet. [Mini Project 2](https://oim6301.github.io/assignments/mini-project-2/) asks you to do the same.

    **CSV** is the plainest table a file can hold: one line per record, commas between the values, and a first line that names the columns.

    First, collect every town. `/ma/counties` lists the 14 counties.
    """)
    return


@app.cell
def _(requests):
    ma_counties = requests.get("https://oim.zhili.dev/ma/counties", timeout=10).json()
    ma_counties[0], len(ma_counties)
    return (ma_counties,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `get_towns` is the function from notebook 4, section 2, with one change: `per_page=100`, because the largest county has 60 towns and the server sends 50 to a page unless you ask for more. Called once per county, it collects every town in the state.
    """)
    return


@app.cell
def _(requests):
    def get_towns(county):
        towns_reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "per_page": 100},
            timeout=10,
        )
        return towns_reply.json()["items"]

    return (get_towns,)


@app.cell
def _(get_towns, ma_counties):
    ma_towns = []
    for _county in ma_counties:
        for _town in get_towns(_county["name"]):
            ma_towns.append(_town)
    len(ma_towns)
    return (ma_towns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Writing the file.** Python's `csv` module writes and reads CSV files, so you never put the commas in yourself. `csv.DictWriter` takes a list of dictionaries, the shape you already have:

    - `fieldnames` names the columns to keep, in order. Each town has 14 fields, and `extrasaction="ignore"` leaves out the ones not named.
    - `.writeheader()` writes the first line, and `.writerows()` writes one line per town.
    - `open(path, "w")` opens the file for writing, and `with` closes it when the block ends. The empty `newline` setting is what the `csv` module asks for, so that lines end the same way on every computer.

    A data file goes in the `data` folder, which sits in the root folder of your repository, one folder up from this notebook.
    """)
    return


@app.cell
def _(csv, ma_towns, mo):
    csv_columns = [
        "name",
        "county",
        "population",
        "income_per_capita_dollars",
        "average_single_family_value_dollars",
        "average_single_family_bill_dollars",
    ]

    ma_towns_csv = mo.notebook_dir().parent / "data" / "ma-towns.csv"
    ma_towns_csv.parent.mkdir(exist_ok=True)

    with open(ma_towns_csv, "w", newline="", encoding="utf-8") as _file:
        _writer = csv.DictWriter(_file, fieldnames=csv_columns, extrasaction="ignore")
        _writer.writeheader()
        _writer.writerows(ma_towns)

    ma_towns_csv.name
    return (ma_towns_csv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Open it.** In VS Code's Explorer, the `data` folder now sits beside the `notebooks` folder, and `ma-towns.csv` is inside it. Click it: the table is plain text, one town per line.

    **Reading it back.** `csv.DictReader` reads one line at a time and turns each into a dictionary, with the header's names as keys. `list(...)` collects them all, and you are back to a list of records, the shape the API sent.
    """)
    return


@app.cell
def _(csv, ma_towns_csv):
    with open(ma_towns_csv, newline="", encoding="utf-8") as _file:
        towns_from_file = list(csv.DictReader(_file))
    len(towns_from_file), towns_from_file[0]
    return (towns_from_file,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Every value the `csv` module reads is text.** Look at the population: `'49831'`, in quotes. A CSV file has no types, only characters, so the module gives you strings, and adding 1 to one raises a `TypeError`. `int()` turns it back into a number, or `float()` when it has a decimal point. The file does not record which columns were numbers, so you convert them yourself.
    """)
    return


@app.cell
def _(towns_from_file):
    towns_from_file[0]["population"], int(towns_from_file[0]["population"])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ A · By Hand

    **No agent for this one**, and no code completion either. When the editor suggests code in grey as you type, press `Esc` and keep typing your own.

    `average_single_family_value_dollars` is the state's figure for what a single-family home in the town is worth on average, as the town assesses it for tax. Call a town a **million-dollar town** when that figure is $1,000,000 or more. Across the state the middle town is near $586,000.

    1. How many million-dollar towns are there, and which county has the most of them? Use `towns_from_file`, a `for` loop, `int()`, and a dictionary that counts, as in notebook 3. *Check yourself: 53 towns, and Middlesex has the most, with 14.*
    2. Which town has the fewest people, and which has the most? Loop over `towns_from_file` and keep the smallest and the largest you have seen so far, the way `find_largest` did in notebook 4. *Check yourself: Gosnold, with 62 people, and Boston, with 673,458.*

    **Going further.** Find the town with the most expensive average home in each county.
    """)
    return


@app.cell
def _(towns_from_file):
    county_counts = {}
    for town in towns_from_file:
        if int(town["average_single_family_value_dollars"]) >= 1000000:
            county=town["county"]
            if county in county_counts:
                county_counts[county] += 1
            else:
                county_counts[county] = 1

    county_counts
    return (county_counts,)


@app.cell
def _(county_counts):
    most_county = None
    most_count = 0
    for _county in county_counts:
        if county_counts[_county] > most_count:
            most_count = county_counts[_county]
            most_county = _county

    most_county, most_count
    return


@app.cell
def _(county_counts):
    total_million_dollar_towns = 0
    for _county in county_counts:
        total_million_dollar_towns += county_counts[_county]

    total_million_dollar_towns
    return


@app.cell
def _(towns_from_file):
    smallest_town = towns_from_file[0]
    largest_town = towns_from_file[0]
    for _town in towns_from_file:
        if int(_town["population"]) < int(smallest_town["population"]):
            smallest_town = _town
        if int(_town["population"]) > int(largest_town["population"]):
            largest_town = _town

    smallest_town["name"], int(smallest_town["population"]), largest_town["name"], int(largest_town["population"])
    return


@app.cell
def _(ma_counties, towns_from_file):
    most_expensive_by_county = {}
    for _county in ma_counties:
        county_name = _county["name"]
        best_town = None
        for _town in towns_from_file:
            if _town["county"] == county_name:
                if best_town is None or int(_town["average_single_family_value_dollars"]) > int(best_town["average_single_family_value_dollars"]):
                    best_town = _town
        most_expensive_by_county[county_name] = best_town["name"]

    most_expensive_by_county
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. Describe What You Want

    Your loops in A spelled out **how**: go through every town, convert, compare, add one or keep the smallest. That took a dozen lines, and a reader has to run them in their head to know what they answer. **polars** lets you describe **what** you want instead.

    `pl.read_csv` reads the same file into a **DataFrame**: a table with named columns. It is your list of records shown as a table, each row a record and each column a key, and polars has already turned the numbers into numbers.
    """)
    return


@app.cell
def _(ma_towns_csv, pl):
    town_table = pl.read_csv(ma_towns_csv)
    town_table
    return (town_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `.schema` lists each column with its type, the step you did with `int()`. `.shape` is the number of rows and columns.
    """)
    return


@app.cell
def _(town_table):
    town_table.schema, town_table.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **A's second step in one line.** `.sort()` puts the rows in order of one column, smallest first, so the first row is the town with the fewest people. `descending=True` puts the largest first.
    """)
    return


@app.cell
def _(town_table):
    town_table.sort("population")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is A's first step in polars. Read it as a sentence:

    - `.filter(...)` keeps the million-dollar towns. It is the `if` in your loop, applied to every row at once, and `pl.col(...)` names the column it reads.
    - `.group_by("county")` makes one group per county, and `.agg(pl.len())` counts the rows in each. It is your counting dictionary.
    - `.sort(..., descending=True)` puts the largest first.
    """)
    return


@app.cell
def _(pl, town_table):
    (
        town_table.filter(pl.col("average_single_family_value_dollars") >= 1_000_000)
        .group_by("county")
        .agg(pl.len().alias("towns"))
        .sort("towns", descending=True)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **A count can mislead.** Middlesex has the most million-dollar towns, and it also has 54 towns, more than any county but Worcester. The fairer question is what share of each county's towns are million-dollar towns.

    - `pl.len()` counts all the towns in each county.
    - A comparison such as `pl.col(...) >= 1_000_000` is `True` or `False` for each town, and `.sum()` adds up the `True`s, which counts them.
    - `.with_columns()` adds a column computed from the others, here one count divided by the other.
    """)
    return


@app.cell
def _(pl, town_table):
    million_dollar_share = (
        town_table.group_by("county")
        .agg(
            pl.len().alias("towns"),
            (pl.col("average_single_family_value_dollars") >= 1_000_000)
            .sum()
            .alias("million_dollar_towns"),
        )
        .with_columns((pl.col("million_dollar_towns") / pl.col("towns")).alias("share"))
        .sort("share", descending=True)
    )
    million_dollar_share
    return (million_dollar_share,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The share tells a different story from the count. Every town in Dukes County, which is Martha's Vineyard and the Elizabeth Islands, and in Nantucket is a million-dollar town, and nearly half of Barnstable's, which is Cape Cod. Middlesex comes sixth.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ B · Check Against the Server

    1. Count every town per county with `town_table`, `.group_by()` and `.agg()`. The server counts them too, in `ma_counties`, and `pl.DataFrame(ma_counties)` turns that list of records into a table. Do the two agree? *Check yourself: Worcester 60, Middlesex 54, Essex 34, and all 14 agree.*
    2. Which five towns of more than 50,000 people have the highest average single-family bill? Use `.filter()`, `.sort()` and `.head()`. *Check yourself: Brookline, Newton, Cambridge, Somerville, Quincy.*

    **Going further.** Ask the towns a question of your own that needs `.filter()`, `.group_by()` and `.sort()` together.
    """)
    return


@app.cell
def _(pl, town_table):
    town_table_county_counts = town_table.group_by("county").agg(pl.len().alias("towns"))
    town_table_county_counts
    return


@app.cell
def _(ma_counties, pl):
    server_county_counts = pl.DataFrame(ma_counties)
    server_county_counts
    return


@app.cell
def _(pl, town_table):
    town_table.filter(pl.col("population") > 50_000).sort("average_single_family_bill_dollars", descending=True).head(5)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Among towns with fewer than 5,000 people, which county has the highest average single-family home value?
    """)
    return


@app.cell
def _(pl, town_table):
    (
        town_table.filter(pl.col("population") < 5_000)
        .group_by("county")
        .agg(pl.col("average_single_family_value_dollars").mean().alias("average_home_value"))
        .sort("average_home_value", descending=True)
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3. The Same Question in SQL

    **This is SQL, a second language, asking A's question once more.** SQL is how databases are asked questions, and from next week the course builds and queries a database. For now, read it; you will write SQL in the database sessions.

    Behind a SQL cell is DuckDB, a database that runs inside the same Python as your notebook. The data stays in your DataFrames. When the cell runs, DuckDB looks up the name in the `FROM` line, here `town_table`, among the notebook's variables and reads that DataFrame as a table. Its answer comes back as a DataFrame too.
    """)
    return


@app.cell
def _(mo, town_table):
    towns_over_threshold = mo.sql(
        f"""
        SELECT county, COUNT(*) AS towns
        FROM town_table
        WHERE average_single_family_value_dollars >= 2000000
        GROUP BY county
        ORDER BY towns DESC
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read it top to bottom: `SELECT` names the columns of the answer, `FROM` the table, `WHERE` keeps some rows, `GROUP BY` makes one group per county, `COUNT(*)` counts each group, and `ORDER BY ... DESC` puts the largest first. Like the polars version, it describes what you want and leaves the how to the computer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ C · Raise the Bar

    In the SQL cell, `1000000` is the bar a town's average home value has to reach. Before you change it to `2000000`, predict in a markdown cell under this question: which counties' counts can go down, and can any go up? Then make the same change in the polars cell that counts million-dollar towns, and run both. *Check yourself: both give Dukes, Middlesex and Norfolk 2 each and Nantucket 1, which is 7 towns.*

    **Going further.** Write a SQL query of your own on `town_table`, and check its answer in polars.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    All of the counties' counts can go down, although they do not have to if all the towns in the county happens to exceed the new bar. However, it's impossible that any of the counties' counts goes up, since raising the bar can only disqualify towns, not qualify new ones.
    """)
    return


@app.cell
def _(mo, town_table):
    high_income_towns = mo.sql(
        f"""
        SELECT name, county, population, income_per_capita_dollars
        FROM town_table
        WHERE population > 20000
        ORDER BY income_per_capita_dollars DESC
        LIMIT 5
        """
    )
    return


@app.cell
def _(pl, town_table):
    town_table.filter(pl.col("population") > 20_000).sort("income_per_capita_dollars", descending=True).head(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 4. The First Chart

    Draw the share. `.plot.bar()` on a DataFrame draws one bar per row, with a library called **altair**. `alt.X()` and `alt.Y()` name each axis's column and give it a title a reader can understand, and `.properties(title=...)` states what the chart shows.

    - Putting the county on `y` lays the bars on their side, so every county's name reads across. `sort="-x"` puts the longest bar first.
    - `axis=alt.Axis(format="%")` writes a share of `0.25` as 25%.

    Wrap it in `mo.ui.altair_chart()`, which is how marimo shows an altair chart of any size.
    """)
    return


@app.cell
def _(alt, million_dollar_share, mo):
    million_dollar_chart = mo.ui.altair_chart(
        million_dollar_share.plot.bar(
            y=alt.Y("county", sort="-x", title="County"),
            x=alt.X(
                "share",
                title="Share of towns averaging $1,000,000 or more",
                axis=alt.Axis(format="%"),
            ),
        ).properties(title="Every town in Dukes and Nantucket averages $1 million or more")
    )
    million_dollar_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `.plot.point()` and `.plot.line()` work the same way. matplotlib is another charting library, and you will meet it in other people's code; [Python §29](https://oim6301.github.io/handbooks/python/03-data/#29-a-chart-with-labeled-axes) shows one chart in each.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## ✏️ D · A Chart of Your Own

    Choose a question one chart can answer, from the data you saved for Mini Project 2 or from `town_table`. Draw it with titled axes, and a title that states what it shows.

    *Check yourself: somebody who has not seen this notebook can say what each axis measures.*

    **Going further.** Color the bars or dots by a column with `color=`, and explain what the colors add.
    """)
    return


@app.cell
def _(alt, mo, town_table):
    income_vs_bill_chart = mo.ui.altair_chart(
        alt.Chart(town_table)
        .mark_circle(opacity=0.6)
        .encode(
            x=alt.X("income_per_capita_dollars", title="Income per capita (dollars)"),
            y=alt.Y("average_single_family_bill_dollars", title="Average single-family tax bill (dollars)"),
            tooltip=["name", "county", "income_per_capita_dollars", "average_single_family_bill_dollars"],
        )
        .properties(title="Towns with higher income per capita tend to pay higher property tax bills")
    )
    income_vs_bill_chart
    return


@app.cell
def _(alt, mo, town_table):
    income_vs_bill_by_county_chart = mo.ui.altair_chart(
        alt.Chart(town_table)
        .mark_circle(opacity=0.6)
        .encode(
            x=alt.X("income_per_capita_dollars", title="Income per capita (dollars)"),
            y=alt.Y("average_single_family_bill_dollars", title="Average single-family tax bill (dollars)"),
            color=alt.Color("county", title="County"),
            tooltip=["name", "county", "income_per_capita_dollars", "average_single_family_bill_dollars"],
        )
        .properties(title="The same towns, colored by county")
    )
    income_vs_bill_by_county_chart
    return


@app.cell
def _(mo):
    mo.md(r"""
    Adding color by county reveals a pattern the first chart hid: towns don't scatter evenly across the plot, they form clusters of the same color. Neighboring towns in the same county tend to share similar income and tax-bill levels, which points to income per capita and property tax bills being shaped more by regional factors, like shared housing markets or municipal budgets, than by each town acting independently.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 This Week's Work

    1. **What is due is listed under *Before next session* in the post-class notes.** I post them on the session page after each class, with the sections we reached, and the checkpoint on Canvas lists the same items.
    2. **[Mini Project 2](https://oim6301.github.io/assignments/mini-project-2/)**, due Sunday 10/25
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Self-check:**

    - [ ] I can save a list of records to a CSV file and read it back with the `csv` module
    - [ ] I can explain why every value the `csv` module reads is text until I convert it
    - [ ] I can read a CSV into a DataFrame and ask it its shape and its column types
    - [ ] I can filter, sort and group a DataFrame
    - [ ] I can read a short SQL query and explain what it asks
    - [ ] I can make one chart from a DataFrame and title its axes
    """)
    return


if __name__ == "__main__":
    app.run()
