from flask import request, render_template, redirect, url_for
from index import app

# 不正なリクエスト
@app.errorhandler(400)
def error_400():
    return render_template("error.html", text="不正なリクエストです")