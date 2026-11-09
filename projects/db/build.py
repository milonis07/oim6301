# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "altair",
# ]
# ///
"""Builds the BabsonAI Labs database from the CSV files in projects/db/data/.
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
    import duckdb
    import polars as pl
    import altair as alt

    return alt, duckdb, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # BabsonAI Labs Database

    This notebook builds `projects/db/database.duckdb` from the CSV files in `projects/db/data/`, every time it runs, so the database always matches those files and the `CREATE TABLE` statements below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Tables

    One `CREATE TABLE` for each table of the ERD in the README, with every primary key and foreign key, and `NOT NULL` and `CHECK` where the scenario's rules call for them.

    Two rules the tables cannot hold with a constraint:

    - "A task is assigned only to somebody who works on its project, and never before that person's start date" needs three tables at once (`tasks`, `assignments`, `people`), and a `CHECK` only sees one row of one table. Checked with a query instead, in `questions.py`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data

    `make_data.py` wrote one CSV per table into `data/`. The cell below deletes any old database file, opens a new one, creates the tables, loads the data, and closes the file when the `with` block ends, so nothing is left open.

    `people` is loaded one row at a time, each manager before the people who report to them. The rows in `people.csv` are already in that order: the two founders first, then the leads, then everybody else. Loading it in one `INSERT ... SELECT` would fail, because DuckDB checks every row's `manager_id` against the table as it was before the statement ran, and a report's manager would not be there yet.
    """)
    return


@app.cell
def _(duckdb, mo, pl):
    data_dir = mo.notebook_dir() / "data"
    database = mo.notebook_dir() / "database.duckdb"

    people_rows = pl.read_csv(data_dir / "people.csv", try_parse_dates=True)
    project_rows = pl.read_csv(data_dir / "projects.csv", try_parse_dates=True)
    assignment_rows = pl.read_csv(data_dir / "assignments.csv", try_parse_dates=True)
    task_rows = pl.read_csv(data_dir / "tasks.csv", try_parse_dates=True)
    expense_rows = pl.read_csv(data_dir / "expenses.csv", try_parse_dates=True)

    database.unlink(missing_ok=True)

    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE people (
                person_id   INTEGER PRIMARY KEY,
                first_name  VARCHAR NOT NULL,
                last_name   VARCHAR NOT NULL,
                work_email  VARCHAR NOT NULL UNIQUE,
                title       VARCHAR NOT NULL,
                start_date  DATE NOT NULL,
                manager_id  INTEGER REFERENCES people(person_id)
            )
        """)
        _con.execute("""
            CREATE TABLE projects (
                project_id   INTEGER PRIMARY KEY,
                name         VARCHAR NOT NULL,
                client_name  VARCHAR,
                category     VARCHAR NOT NULL CHECK (category IN ('LLM app', 'data pipeline', 'internal tool')),
                budget       DECIMAL(12, 2) NOT NULL CHECK (budget > 0),
                start_date   DATE NOT NULL,
                status       VARCHAR NOT NULL CHECK (status IN ('planned', 'active', 'paused', 'done'))
            )
        """)
        _con.execute("""
            CREATE TABLE assignments (
                person_id       INTEGER NOT NULL REFERENCES people(person_id),
                project_id      INTEGER NOT NULL REFERENCES projects(project_id),
                role            VARCHAR NOT NULL,
                hours_per_week  INTEGER NOT NULL CHECK (hours_per_week BETWEEN 1 AND 40),
                joined_date     DATE NOT NULL,
                PRIMARY KEY (person_id, project_id)
            )
        """)
        _con.execute("""
            CREATE TABLE tasks (
                task_id         INTEGER PRIMARY KEY,
                project_id      INTEGER NOT NULL REFERENCES projects(project_id),
                description     VARCHAR NOT NULL,
                created_date    DATE NOT NULL,
                assigned_to     INTEGER REFERENCES people(person_id),
                due_date        DATE NOT NULL,
                completed_date  DATE,
                CHECK (completed_date IS NULL OR completed_date >= created_date)
            )
        """)
        _con.execute("""
            CREATE TABLE expenses (
                expense_id    INTEGER PRIMARY KEY,
                project_id    INTEGER NOT NULL REFERENCES projects(project_id),
                expense_date  DATE NOT NULL,
                amount        DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
                category      VARCHAR NOT NULL CHECK (category IN ('GPU cloud', 'data labeling', 'software', 'travel')),
                note          VARCHAR
            )
        """)

        for _row in people_rows.iter_rows(named=True):
            _con.execute(
                "INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    _row["person_id"],
                    _row["first_name"],
                    _row["last_name"],
                    _row["work_email"],
                    _row["title"],
                    _row["start_date"],
                    _row["manager_id"],
                ],
            )

        _con.execute("INSERT INTO projects SELECT * FROM project_rows")
        _con.execute("INSERT INTO assignments SELECT * FROM assignment_rows")
        _con.execute("INSERT INTO tasks SELECT * FROM task_rows")
        _con.execute("INSERT INTO expenses SELECT * FROM expense_rows")

        _con.execute("""
            CREATE VIEW project_status AS
                SELECT
                    p.project_id,
                    p.name,
                    p.status,
                    p.budget,
                    coalesce(sum(e.amount), 0) AS spent,
                    round(coalesce(sum(e.amount), 0) * 100.0 / p.budget, 1) AS percent_spent,
                    count(DISTINCT t.task_id) AS total_tasks,
                    count(DISTINCT CASE WHEN t.completed_date IS NULL THEN t.task_id END) AS open_tasks,
                    count(DISTINCT CASE WHEN t.completed_date IS NULL AND t.due_date < current_date THEN t.task_id END) AS overdue_tasks
                FROM projects p
                LEFT JOIN expenses e ON e.project_id = p.project_id
                LEFT JOIN tasks t ON t.project_id = p.project_id
                GROUP BY p.project_id, p.name, p.status, p.budget
        """)

    database.name
    return (database,)


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. A Look at the Data

    Tasks by the day of the week they were created, read straight from `tasks.csv` with polars.
    """)
    return


@app.cell
def _(alt, mo, pl):
    _day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    _tasks = pl.read_csv(mo.notebook_dir() / "data" / "tasks.csv", try_parse_dates=True)
    _tasks_by_day = (
        _tasks.with_columns(pl.col("created_date").dt.strftime("%a").alias("day"))
        .group_by("day")
        .agg(pl.len().alias("tasks"))
    )
    alt.Chart(_tasks_by_day).mark_bar().encode(
        x=alt.X("day", sort=_day_order), y="tasks"
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A real business opens most of its tasks on weekdays. The chart shows almost none on Saturday or Sunday, because `make_data.py` pulls any weekend `created_date` back to the Friday before, after an earlier version of the script spread task creation evenly across all seven days.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Row Counts
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT 'people' AS table_name, count(*) AS rows FROM people
        UNION ALL SELECT 'projects', count(*) FROM projects
        UNION ALL SELECT 'assignments', count(*) FROM assignments
        UNION ALL SELECT 'tasks', count(*) FROM tasks
        UNION ALL SELECT 'expenses', count(*) FROM expenses
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses

    `ask()` only reads, so this insert opens a write connection of its own, inside `try`/`except`, so the rest of the notebook keeps running. A budget of -500 breaks `CHECK (budget > 0)`.
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute(
                "INSERT INTO projects VALUES (999, 'Bad Budget Project', NULL, 'internal tool', -500, '2026-01-01', 'planned')"
            )
        budget_check = "accepted"
    except duckdb.ConstraintException as _error:
        budget_check = str(_error).splitlines()[0]
    budget_check
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew

    **1. How many people work at BabsonAI Labs?** Expected: 25, because `make_data.py` sets `NUM_PEOPLE = 25`.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS people FROM people")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **2. How many projects have no expenses at all?** Expected: 2, because `make_data.py` deliberately leaves two planned projects with no expense rows.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT project_id, name, status
        FROM projects
        WHERE project_id NOT IN (SELECT DISTINCT project_id FROM expenses)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **3. How many people report to nobody?** Expected: 2, the two founders, because the scenario says "the two founders report to nobody."
    """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) AS people_with_no_manager FROM people WHERE manager_id IS NULL")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View

    `project_status`, saved in the cell that builds the database, is the question BabsonAI Labs would ask every week: how much of each project's budget is spent, and how many of its tasks are open or overdue.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM project_status ORDER BY percent_spent DESC")
    return


if __name__ == "__main__":
    app.run()
