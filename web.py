from flask import Flask, render_template
from hollister_data import HollisterData
from stats import Stats


data_collector = HollisterData()
stats_data = Stats()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", stats_data=stats_data.items_stats)


@app.route("/item/<item_id>")
def item_detail(item_id):
    data_for_web = data_collector.find_by_id(item_id)
    return render_template("item_price_history.html", selected_idem_data=data_for_web)


if __name__ == "__main__":
    app.run(debug=True)
