from flask import Flask, render_template
from hollister_data import HollisterData
from stats import Stats


data_collector = HollisterData()
stats_data = Stats()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", stats_data=stats_data.items_stats)


if __name__ == "__main__":
    app.run(debug=True)
