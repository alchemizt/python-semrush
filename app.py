# app.py
from semrush_api import get_serp_data, get_keyword_volume

keyword = "python tutorial"

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    if request.method == "POST":
        keyword = request.form["keyword"]
        data = get_serp_data(keyword)

        # Get Keyword Volume
        volume_data = get_keyword_volume(keyword)
        print(f"Keyword Volume for '{keyword}':\n", volume_data)

        return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
