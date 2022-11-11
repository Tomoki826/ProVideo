from flask import request, render_template
from main import app, api_key
from main.models.TMDB import TMDB
from main.models.genre import Genre
from main.models.enum import Search
import datetime, re

# 映画・ドラマの検索ページ
@app.route("/", methods=["GET", "POST"])
def index():
       if request.method == 'GET':
              keywords = "テスト"
              page = 1
       if request.method == 'POST':
              keywords = request.form.get('keywords')
              page = 1
       
       # TMDBで検索する
       search_type = Search.MOVIES
       if (search_type == Search.MOVIES):
              soup = TMDB(api_key).search_movies(keywords, page)
       elif (search_type == Search.TVSHOWS):
              soup = TMDB(api_key).search_tvshows(keywords, page)
       elif (search_type == Search.MULTI):
              soup = TMDB(api_key).search_multi(keywords, page)
       elif (search_type == Search.SENSITIVE):
              soup = TMDB(api_key).search_multi(keywords, page, True)
       # 検索結果の整理
       data = soup
       data = result_arrangement(keywords, page, data)
       # 検索エラーチェック
       if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
              return render_template("index.html", data=data, error=True)
       # 検索結果を表示
       return render_template("index.html", data=data, error=False)

# 検索情報をフォーマットする
def result_arrangement(keywords, page, data={}):
       data['keywords'] = keywords
       data['current_page'] = page
       for item in data['results']:
              if 'adult' not in item:
                     item['adult'] = 'false'
              if 'title' not in item:
                     item['title'] = '(タイトル情報なし)'
              if 'release_date' not in item:
                     item['release_date'] = '公開日: 不明'
              else:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['release_date']):
                            dte = datetime.datetime.strptime(item['release_date'], '%Y-%m-%d')
                            item['release_date'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
                     else:
                            pass
                            item['release_date'] = '公開日: 不明'
              # ジャンル
              if 'genre_ids' not in item or item.get('genre_ids') == []:
                     item['genre'] = 'ジャンル: 不明'
              else:
                     item['genre'] = 'ジャンル: '
                     for id in item['genre_ids']:
                             item['genre'] += Genre().name_get(id) + ' '
                     item['genre'] = item['genre'][:-1]
              item.pop('genre_ids', None)
       return data