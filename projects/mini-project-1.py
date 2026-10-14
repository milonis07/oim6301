# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*

    The coffee shop manager could use this analysis to decide when to reorder oat milk to meet customer demand while maintaining appropriate stock levels. Since deliveries take three days and daily demand varies, ordering too late could result in lost sales, while ordering too early could lead to excess inventory. By comparing different reorder points, I want to find the most suitable option that balances product availability with inventory costs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    I would start with 60 cartons of oat milk and go through the 30 days one by one. At the start of each day, I would check if any orders placed earlier have arrived and add those cartons to the current stock. Then, I would compare the available stock with the day's demand to figure out how many cartons can be sold and how many sales would be lost if there isn't enough stock. At the end of the day, I would update the remaining stock and check if the stock available, including orders that are still on the way, is less than or equal to the reorder point. If it is, I would place an order for another 100 cartons, which would arrive three days later. I would repeat this for all 30 days and test the four reorder points: 20, 30, 40, and 50. Finally, I would compare the results to see which reorder point works best for the coffee shop.

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*

    - The loop carries the remaining stock from one day to the next, so the ending stock of one day becomes the starting stock for the next. It also keeps track of orders that are still on the way so that they are added to the stock when they arrive.

    - *Which check will you use in section 6, and which two numbers should agree?*

    I would check whether the total demand equals the total cartons sold plus the total units lost. These numbers should be equal because all the cartons customers ask for must either be sold or counted as lost sales.

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Starting inventory and ordering details
    starting_stock = 60
    order_quantity = 100
    lead_time_days = 3

    # Reorder points to compare
    reorder_points = [20, 30, 40, 50]

    # Daily demand for 30 days
    daily_demand = [
        12, 15, 9, 14, 18, 11, 10, 16, 13, 17,
        8, 12, 20, 14, 11, 9, 15, 13, 16, 12,
        10, 14, 19, 11, 13, 15, 9, 12, 17, 14
    ]

    return (
        daily_demand,
        lead_time_days,
        order_quantity,
        reorder_points,
        starting_stock,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(daily_demand, lead_time_days, order_quantity, starting_stock):
    def simulate(reorder_point):
        stock = starting_stock
        pending_orders = []
        rows = []

        total_lost = 0
        days_with_lost_sales = 0
        orders_placed = 0
        total_ending_stock = 0

        for day in range(1, len(daily_demand) + 1):
            starting = stock
            arrived = 0
            remaining_orders = []

            # Receive orders that are due today.
            for arrival_day, quantity in pending_orders:
                if arrival_day == day:
                    arrived += quantity
                else:
                    remaining_orders.append((arrival_day, quantity))

            pending_orders = remaining_orders
            stock = stock + arrived

            # Sell what is available and record lost sales.
            demand = daily_demand[day - 1]
            sold = min(stock, demand)
            lost = demand - sold
            stock = stock - sold

            total_lost += lost
            if lost > 0:
                days_with_lost_sales += 1

            # Count stock plus orders that have not arrived.
            inventory_position = stock
            for arrival_day, quantity in pending_orders:
                inventory_position += quantity

            # Place an order if the reorder point is reached.
            ordered = 0
            if inventory_position <= reorder_point:
                ordered = order_quantity
                pending_orders.append(
                    (day + lead_time_days, order_quantity)
                )
                orders_placed += 1

            ending = stock
            total_ending_stock += ending

            rows.append({
                "day": day,
                "starting": starting,
                "arrived": arrived,
                "demand": demand,
                "sold": sold,
                "lost": lost,
                "ending": ending,
                "ordered": ordered
            })

        average_stock = total_ending_stock / len(daily_demand)

        return (
            rows,
            total_lost,
            days_with_lost_sales,
            orders_placed,
            average_stock
        )


    return (simulate,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(simulate):

    result = simulate(40)
    daily_rows = result[0]

    print("DAILY SIMULATION: REORDER POINT 40")
    print(
        f"{'Day':>3} {'Start':>7} {'Arrived':>7} "
        f"{'Demand':>7} {'Sold':>6} {'Lost':>6} "
        f"{'Ending':>7} {'Ordered':>8}"
    )

    for row in daily_rows:
        print(
            f"{row['day']:>3} "
            f"{row['starting']:>7} "
            f"{row['arrived']:>7} "
            f"{row['demand']:>7} "
            f"{row['sold']:>6} "
            f"{row['lost']:>6} "
            f"{row['ending']:>7} "
            f"{row['ordered']:>8}"
        )

    return


@app.cell
def _(reorder_points, simulate):

    print("\nREORDER POINT COMPARISON")
    print(
        f"{'Point':>6} {'Units Lost':>11} "
        f"{'Lost Days':>10} {'Orders':>7} "
        f"{'Avg Stock':>10}"
    )

    for point in reorder_points:
        comparison_result = simulate(point)

        print(
            f"{point:>6} "
            f"{comparison_result[1]:>11} "
            f"{comparison_result[2]:>10} "
            f"{comparison_result[3]:>7} "
            f"{comparison_result[4]:>10.2f}"
        )

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(daily_demand, simulate):
    
    check_rows = simulate(40)[0]

    total_demand = sum(daily_demand)
    total_sold = 0
    total_lost = 0
    inventory_balances = True

    for row in check_rows:
        total_sold += row["sold"]
        total_lost += row["lost"]

        expected_ending = (
            row["starting"] + row["arrived"] - row["sold"]
        )

        if expected_ending != row["ending"]:
            inventory_balances = False

    print("Total demand:", total_demand)
    print("Total sold + total lost:", total_sold + total_lost)
    print("Demand check:", total_demand == total_sold + total_lost)
    print("Daily inventory balance check:", inventory_balances)

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
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
