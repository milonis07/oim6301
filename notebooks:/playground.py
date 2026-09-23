import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    charge = 10
    return (charge,)


@app.cell
def _(charge):
    print(charge)
    return


if __name__ == "__main__":
    app.run()
