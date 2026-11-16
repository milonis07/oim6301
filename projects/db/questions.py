# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "altair",
# ]
# ///
"""Asks projects/db/database.duckdb the BabsonAI Labs business questions.
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
    from datetime import date

    import altair as alt
    import duckdb
    import polars as pl

    return alt, date, duckdb, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # BabsonAI Labs: Business Questions

    This notebook asks `database.duckdb`, built by `build.py`, the eight questions on scenario A's list and two of my own.
    """)
    return


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, database


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **One date for every question.** `as_of` is the one date everything below counts back from: "last 90 days" is the 90 days ending on `as_of`, and "last month" would be the last full calendar month before it.
    """)
    return


@app.cell
def _(date):
    as_of = date(2026, 11, 8)
    as_of
    return (as_of,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    *(This section is answered out of order on purpose: the assignment asks me to pick the question below and write my prediction before I answer any of the ten questions, so the prediction below was written, and committed as `db: prediction`, before a single query further down this notebook was run.)*

    **The question I picked:** Question 6, "One row per project with its number of tasks and its total expenses, each checked against counting it on its own." It needs three tables: `projects`, `tasks` and `expenses`.

    **My prediction.** `make_data.py` gives every one of the 14 projects exactly `TARGET_TASKS // NUM_PROJECTS = 300 // 14 = 21` tasks, so there are `14 \u00d7 21 = 294` tasks in all. It gives expenses to 12 of the 14 projects (2 are left with none on purpose), splitting `TARGET_EXPENSES // 12 = 220 // 12 = 18` expenses across each of those 12, so `12 \u00d7 18 = 216` expenses in all.

    If I join `tasks` straight to `expenses` on `project_id`, before any `GROUP BY`, every task row pairs with every expense row that shares its project, so one project with expenses contributes `21 \u00d7 18 = 378` rows, and the 2 projects with no expenses contribute `21 \u00d7 0 = 0` rows each. I expect the join, counted before grouping, to come to `12 \u00d7 378 = 4,536` rows, not 294 (the number of tasks) and not 216 (the number of expenses).
    """)
    return
