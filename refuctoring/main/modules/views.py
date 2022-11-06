from flask import render_template
from main import app

# 映画・ドラマの検索ページ
@app.route("/", methods=["GET"])
def index():
       return render_template("index.html")