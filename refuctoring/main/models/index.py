from flask import render_template
from main import app, api_key
from main.models.TMDB import TMDB
from main.models.enum import Search

# 映画・ドラマの検索ページ
@app.route("/", methods=["GET"])
def index():
       # TMDBで検索する
       keywords = "カイジ"
       page = 1
       search_type = Search.MOVIES
       if (search_type == Search.MOVIES):
              soup = TMDB(api_key).search_movies(keywords, page)
       elif (search_type == Search.TVSHOWS):
              soup = TMDB(api_key).search_tvshows(keywords, page)
       elif (search_type == Search.MULTI):
              soup = TMDB(api_key).search_multi(keywords, page)
       elif (search_type == Search.SENSITIVE):
              soup = TMDB(api_key).search_multi(keywords, page, True)
       # 検索エラーチェック
       if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
              return render_template("index.html", data={}, error=True)
       # 検索結果の整理
       return render_template("index.html", data=soup, error=False)