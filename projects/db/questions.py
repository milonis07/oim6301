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
    ## Question 1: Each Project's Expenses Against Its Budget

    Uses the `project_status` view built in `build.py`.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT project_id, name, status, budget, spent, percent_spent
        FROM project_status
        ORDER BY percent_spent DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Project 14, *Visionary secondary Graphical User Interface*, has spent the largest share of its budget: 84.2%, or $80,806.46 of its $95,915.72. Projects 7 and 13 sit at the other end, at 0.0%, because they have not spent anything yet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 2: Tasks Past Due and Not Completed

    Three tables: `tasks`, `projects` and `people`.
    """)
    return


@app.cell
def _(ask, as_of):
    ask(f"""
        SELECT t.task_id, p.name AS project_name,
               pe.first_name || ' ' || pe.last_name AS assigned_to,
               t.due_date
        FROM tasks t
        JOIN projects p ON p.project_id = t.project_id
        JOIN people pe ON pe.person_id = t.assigned_to
        WHERE t.completed_date IS NULL AND t.due_date < DATE '{as_of.isoformat()}'
        ORDER BY t.due_date
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    127 tasks are past their due date and still not completed. The oldest is task 2, on project *Multi-layered heuristic database*, assigned to Cynthia Diaz and due 2025-10-09.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 3: Each Person's Hours a Week Across Active Projects
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT a.person_id, pe.first_name, pe.last_name, sum(a.hours_per_week) AS total_hours
        FROM assignments a
        JOIN projects p ON p.project_id = a.project_id
        JOIN people pe ON pe.person_id = a.person_id
        WHERE p.status = 'active'
        GROUP BY a.person_id, pe.first_name, pe.last_name
        ORDER BY total_hours DESC
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT a.person_id, pe.first_name, pe.last_name, sum(a.hours_per_week) AS total_hours
        FROM assignments a
        JOIN projects p ON p.project_id = a.project_id
        JOIN people pe ON pe.person_id = a.person_id
        WHERE p.status = 'active'
        GROUP BY a.person_id, pe.first_name, pe.last_name
        HAVING sum(a.hours_per_week) > 40
        ORDER BY total_hours DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    16 people have an active-project assignment. Of those, 3 commit more than 40 hours a week across their active projects combined: Patricia Miller at 95 hours, Jeffery Wagner at 71, and Danielle Johnson at 46.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 4: Expenses by Category, Last 90 Days, Above the Category Average
    """)
    return


@app.cell
def _(ask, as_of):
    ask(f"""
        SELECT category, sum(amount) AS total
        FROM expenses
        WHERE expense_date BETWEEN DATE '{as_of.isoformat()}' - INTERVAL 90 DAY AND DATE '{as_of.isoformat()}'
        GROUP BY category
        ORDER BY total DESC
    """)
    return


@app.cell
def _(ask, as_of):
    ask(f"""
        WITH category_totals AS (
            SELECT category, sum(amount) AS total
            FROM expenses
            WHERE expense_date BETWEEN DATE '{as_of.isoformat()}' - INTERVAL 90 DAY AND DATE '{as_of.isoformat()}'
            GROUP BY category
        )
        SELECT category, total
        FROM category_totals
        WHERE total > (SELECT avg(total) FROM category_totals)
        ORDER BY total DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Over the 90 days ending 2026-11-08, the four categories average $94,821.46 each. Two categories are above that average: software, at $114,484.22, and GPU cloud, at $99,604.02; data labeling and travel both fall below it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 5: Projects With No Expenses At All
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
    Two projects have no expenses at all: project 7, *Re-contextualized transitional functionalities*, and project 13, *Reactive 24/7 software*. Both are still `planned`, so nothing has been spent on either yet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 6: Tasks and Expenses, Per Project

    Three tables: `projects`, `tasks` and `expenses`. Joining `tasks` straight to `expenses` on `project_id` would multiply every task by every expense on the same project, so this counts each one in its own subquery instead, and the cell after it checks both totals against counting the rows directly.
    """)
    return


@app.cell
def _(ask):
    ask("""
        WITH task_counts AS (
            SELECT project_id, count(*) AS task_count FROM tasks GROUP BY project_id
        ),
        expense_totals AS (
            SELECT project_id, sum(amount) AS total_expenses FROM expenses GROUP BY project_id
        )
        SELECT p.project_id, p.name,
               coalesce(tc.task_count, 0) AS task_count,
               coalesce(et.total_expenses, 0) AS total_expenses
        FROM projects p
        LEFT JOIN task_counts tc ON tc.project_id = p.project_id
        LEFT JOIN expense_totals et ON et.project_id = p.project_id
        ORDER BY p.project_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every project has exactly 21 tasks; the 12 projects with expenses each total somewhere between $58,107 and $82,496, and projects 7 and 13 show $0, matching question 5's answer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 7: Every Task Checked Against the Assignment Rule *(checks a rule)*

    Three tables: `tasks`, `people` and `assignments`. A task breaks the rule if its assignee has no row in `assignments` for that project, or if the task was created before that person's `start_date`.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT t.task_id, t.project_id,
               pe.first_name || ' ' || pe.last_name AS assignee,
               t.created_date, pe.start_date
        FROM tasks t
        JOIN people pe ON pe.person_id = t.assigned_to
        LEFT JOIN assignments a ON a.person_id = t.assigned_to AND a.project_id = t.project_id
        WHERE t.assigned_to IS NOT NULL
          AND (a.person_id IS NULL OR t.created_date < pe.start_date)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two tasks break the rule, the same two `make_data.py` breaks on purpose: task 1 is assigned to Danielle Johnson, who does not work on project 1 at all, and task 2 is assigned to Cynthia Diaz, who works on project 1 but was created on 2025-09-25, 10 days before her start date of 2025-10-05.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 8: Direct Reports and Their Hours, By Manager

    Three tables: `people` joined to itself for the manager/report relationship, and `assignments` for the hours.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT m.person_id, m.first_name, m.last_name,
               count(DISTINCT r.person_id) AS direct_reports,
               coalesce(sum(a.hours_per_week), 0) AS total_hours
        FROM people m
        JOIN people r ON r.manager_id = m.person_id
        LEFT JOIN assignments a ON a.person_id = r.person_id
        GROUP BY m.person_id, m.first_name, m.last_name
        ORDER BY direct_reports DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Robert Johnson has the most direct reports, 8, who together commit 354 hours a week across all their projects, the most of any manager's team.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 9: Which Project Category Has the Most Money Committed Right Now? *(my own question)*

    A manager deciding where to put the next hire would ask this: of the projects actually running today, which category of work is the company's money tied up in?
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT category, count(*) AS project_count, sum(budget) AS total_budget
        FROM projects
        WHERE status = 'active'
        GROUP BY category
        ORDER BY total_budget DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of the 6 active projects, internal tool work holds the most committed budget, $1,207,676.02 across 5 projects, next to a single active data pipeline project at $458,305.34; no LLM app project is active right now.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Question 10: Which Projects Have Fallen Behind on Their Tasks? *(my own question)*

    A manager would want to know which projects need attention before they fall further behind, measured by the share of tasks actually marked done.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT p.project_id, p.name,
               count(t.task_id) AS total_tasks,
               count(t.completed_date) AS completed_tasks,
               round(count(t.completed_date) * 100.0 / count(t.task_id), 1) AS completion_rate_percent
        FROM projects p
        JOIN tasks t ON t.project_id = p.project_id
        GROUP BY p.project_id, p.name
        HAVING count(t.completed_date) * 1.0 / count(t.task_id) < 0.5
        ORDER BY completion_rate_percent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    7 of the 14 projects have completed less than half of their 21 tasks. Project 5, *Visionary zero-defect approach*, is furthest behind, with only 6 of 21 tasks (28.6%) completed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 1: How I Know These Numbers Are Right

    Two of the answers above are reached a second way, and both checks fail loudly if the numbers stop agreeing.
    """)
    return


@app.cell
def _(ask):
    _view_total = ask("SELECT sum(spent) AS total FROM project_status")["total"][0]
    _direct_total = ask("SELECT sum(amount) AS total FROM expenses")["total"][0]
    assert _view_total == _direct_total, f"{_view_total} != {_direct_total}"
    spent_check = (_view_total, _direct_total, "agree")
    spent_check
    return


@app.cell
def _(ask):
    _view_total = ask("SELECT sum(total_tasks) AS total FROM project_status")["total"][0]
    _direct_total = ask("SELECT count(*) AS total FROM tasks")["total"][0]
    assert _view_total == _direct_total, f"{_view_total} != {_direct_total}"
    task_count_check = (_view_total, _direct_total, "agree")
    task_count_check
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `project_status.spent`, summed across all 14 projects, is $865,898.59, the same as summing `expenses.amount` directly; and `project_status.total_tasks`, summed the same way, is 294, the same as `count(*)` on `tasks` directly. Both `assert`s above would raise if that stopped being true, which is exactly what happened the first time I built this view: see "Working With the Agent" below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 2: Working With the Agent

    Building question 1's query against the `project_status` view, I expected `percent_spent` to stay under 100% for most projects, but every active project showed numbers like 1,769.2% and 1,465.9%. My agent's first version of that view, in `build.py`, computed `spent` as `sum(e.amount)` after joining `projects` to both `expenses` and `tasks` in the same query. Because every project has 21 tasks, each expense row was being matched against all 21 of that project's task rows and counted 21 times over, the same fan-out question 6 above exists to guard against.

    I caught it by comparing `project_status`'s total against `SELECT sum(amount) FROM expenses` directly, the same check now in the cell above: $865,898.59 direct against roughly $18.2M through the view, more than 21x too high. I had my agent rewrite the view to pre-aggregate `expenses` and `tasks` into their own one-row-per-project subqueries before joining either to `projects`, so no row gets matched against more than one row of the other table, and reran the check until the two totals matched exactly. That fix is committed as `db: fix project_status fan-out bug found while answering Part B Q1`, in the `CREATE VIEW project_status` cell of `build.py`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 3: Reading It Back

    *(This section is answered out of order on purpose: the assignment asks me to pick the question below and write my prediction before I answer any of the ten questions, so the prediction below was written, and committed as `db: prediction`, before a single query further down this notebook was run.)*

    **The question I picked:** Question 6, "One row per project with its number of tasks and its total expenses, each checked against counting it on its own." It needs three tables: `projects`, `tasks` and `expenses`.

    **My prediction.** `make_data.py` gives every one of the 14 projects exactly `TARGET_TASKS // NUM_PROJECTS = 300 // 14 = 21` tasks, so there are `14 \u00d7 21 = 294` tasks in all. It gives expenses to 12 of the 14 projects (2 are left with none on purpose), splitting `TARGET_EXPENSES // 12 = 220 // 12 = 18` expenses across each of those 12, so `12 \u00d7 18 = 216` expenses in all.

    If I join `tasks` straight to `expenses` on `project_id`, before any `GROUP BY`, every task row pairs with every expense row that shares its project, so one project with expenses contributes `21 \u00d7 18 = 378` rows, and the 2 projects with no expenses contribute `21 \u00d7 0 = 0` rows each. I expect the join, counted before grouping, to come to `12 \u00d7 378 = 4,536` rows, not 294 (the number of tasks) and not 216 (the number of expenses).
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT count(*) AS joined_rows
        FROM tasks t
        JOIN expenses e ON t.project_id = e.project_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The join produces exactly 4,536 rows, matching my prediction. That confirms the fan-out: joining `tasks` to `expenses` directly multiplies each project's task count by its expense count, which is why question 6's own answer counts each table in its own subquery instead, and it is the same bug the "Working With the Agent" section above describes finding in `project_status`.

    **What one row of this join means.** One row of `tasks JOIN expenses ON project_id`, before any grouping, is not a fact about the business at all: it is one task paired with one expense that merely happen to belong to the same project, with no real relationship between that task and that expense. That is exactly why this join is the wrong way to answer question 6, and why the real answer uses two separate subqueries instead.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 4: Going Further

    Two things past the ten questions:

    1. **A chart.** Question 1's answer as a bar chart, both axes titled, so the budget picture is visible at a glance instead of read row by row.
    2. **A control.** A dropdown of projects that changes what a query returns, so anybody can look up one project's open tasks without touching the code.
    """)
    return


@app.cell
def _(alt, ask):
    _project_status = ask("SELECT name, percent_spent FROM project_status ORDER BY percent_spent DESC")
    alt.Chart(_project_status).mark_bar().encode(
        x=alt.X("percent_spent", title="Percent of budget spent"),
        y=alt.Y("name", sort="-x", title="Project"),
    )
    return


@app.cell
def _(ask, mo):
    _projects = ask("SELECT project_id, name FROM projects ORDER BY name")
    project_picker = mo.ui.dropdown(
        options=dict(zip(_projects["name"], _projects["project_id"])),
        value=_projects["name"][0],
        label="Project",
    )
    project_picker
    return (project_picker,)


@app.cell
def _(ask, project_picker):
    ask(f"""
        SELECT task_id, description, due_date, completed_date
        FROM tasks
        WHERE project_id = {project_picker.value} AND completed_date IS NULL
        ORDER BY due_date
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both work: the chart makes project 14's 84.2% jump out without reading the table row by row, and the dropdown above swaps which project's open tasks the last cell shows without editing any SQL.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 5: Time Spent

    About 8 hours outside class.
    """)
    return


if __name__ == "__main__":
    app.run()
