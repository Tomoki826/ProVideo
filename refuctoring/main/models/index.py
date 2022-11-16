from flask import request, render_template, redirect, url_for
from main import app, api_key
from main.models.TMDB import TMDB
from main.models.genre import Genre
from main.models.enum import Search
import datetime, re

# 成人向けを検索結果に含めるか？
sensitive_search = True

# ホームページ
@app.route("/", methods=["GET", "POST"])
def index(search_type=int(Search.DISCOVER_MOVIE)):
       # 話題の映画を取得
       page = 1
       soup = TMDB(api_key).discover_movie(page)
       # 検索結果の整理
       data = soup
       data = result_arrangement(search_type, page, data)
       data['max_page'] = 1
       data['total_results'] = min(20, data['total_results'])
       # 検索エラーチェック
       if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
              return render_template("error.html")
       # 話題のテレビ・配信番組を取得
       page = 1
       soup2 = TMDB(api_key).discover_tvshows(page)
       # 検索結果の整理
       data2 = soup2
       data2 = result_arrangement(search_type, page, data2)
       data2['max_page'] = 1
       data2['total_results'] = min(20, data2['total_results'])
       # 検索エラーチェック
       if 'errors' in soup2 or soup2['results'] == [] or soup2['total_results'] <= 0:
              return render_template("error.html")
       # 検索結果を表示
       return render_template("home.html", data=data, data2=data2, soup=soup)

# 作品を検索
@app.route("/search", methods=["GET"])
def search():
       # パラメータチェック
       if 'keywords' in request.args:
              keywords = request.args['keywords']
              print(len(keywords))
              if len(keywords) == 0: keywords = ' '
       else:
              return render_template("error.html")
       if 'page' in request.args:
              page = int(request.args['page'])
              if page <= 0: page = 1
       else:
              page = 1
       if 'search_type' in request.args:
              search_type = int(request.args['search_type'])
              if not (1 <= search_type and search_type <= 4):
                     return render_template("error.html")
       else:
              search_type = Search.MULTI
       # TMDBで検索する
       if (search_type == Search.MOVIES):
              soup = TMDB(api_key).search_movies(keywords, page)
       elif (search_type == Search.TVSHOWS):
              soup = TMDB(api_key).search_tvshows(keywords, page)
       elif (search_type == Search.MULTI):
              soup = TMDB(api_key).search_multi(keywords, page, sensitive_search)
       elif (search_type == Search.PERSON):
              soup = TMDB(api_key).search_person(keywords, page, sensitive_search)
       # 検索結果の整理
       data = soup
       data = result_arrangement(search_type, page, data, keywords)
       # 検索エラーチェック
       #if 'errors' in soup or soup['results'] == [] or soup['total_results'] <= 0:
       #       return render_template("error.html")
       # 検索結果を表示
       return render_template("index.html", data=data, soup=soup, error=False)


# 検索情報をフォーマットする
def result_arrangement(search_type, page, in_data, keywords=''):
       data = {}
       data['keywords'] = keywords
       data['current_page'] = page
       data['max_page'] = (in_data['total_results'] - 1) // 20 + 1
       data['total_results'] = in_data['total_results']
       # (人物のデータは取り除く)
              # ※取り除くとページ番号や検索数がずれるのでキャストごとについかするか検討中
       # 検索タイプ
       data['search_type'] = search_type
       if search_type == Search.MOVIES or search_type == Search.TVSHOWS or search_type == Search.MULTI or search_type == Search.PERSON:
              data['search_type-btn'] = int(search_type)
       else:
              data['search_type-btn'] = int(Search.MULTI)
       # 検索データの整理
       data['results'] = []
       for item in in_data['results']:
              li_data = {}
              # 作品タイトル
              if 'adult' not in item:
                     li_data['adult'] = 'false'
              if 'title' in item:
                     li_data['title'] = item['title']
              elif 'name' in item:
                     li_data['title'] = item['name']
              elif 'original_name' in item:
                     li_data['title'] = item['original_name']
              else:
                     li_data['title'] = '(タイトル情報なし)'
              # 公開日
              if 'release_date' in item:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['release_date']):
                            dte = datetime.datetime.strptime(item['release_date'], '%Y-%m-%d')
                            li_data['openday'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
              elif 'first_air_date' in item:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['first_air_date']):
                            dte = datetime.datetime.strptime(item['first_air_date'], '%Y-%m-%d')
                            li_data['openday'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
              if 'openday' not in li_data:
                     li_data['openday'] = '公開日: 不明'
              # ジャンル
              if 'genre_ids' not in item or item.get('genre_ids') == []:
                     li_data['genre'] = 'ジャンル: 不明'
              else:
                     li_data['genre'] = 'ジャンル: '
                     for id in item['genre_ids']:
                             li_data['genre'] += Genre().name_get(id) + ' '
                     li_data['genre'] = li_data['genre'][:-1]
              # ポスター画像
              if 'poster_path' in item:
                     li_data['poster_path'] = item['poster_path']
              else:
                     li_data['poster_path'] = ''
              # メディアタイプ
              match search_type:
                     case Search.MOVIES:
                            li_data['media_type'] = '映画'
                     case Search.TVSHOWS:
                            li_data['media_type'] = 'テレビ・配信番組'
                     case Search.PERSON:
                            li_data['media_type'] = '人物'
                     case Search.MULTI:
                            if 'media_type' not in item:
                                   li_data['media_type'] = '不明'
                            elif item.get('adult') == True:
                                   li_data['media_type'] = 'アダルト'
                            else:
                                   match item['media_type']:
                                          case 'movie':
                                                 li_data['media_type'] = '映画'
                                          case 'tv':
                                                 li_data['media_type'] = 'テレビ・配信番組'
                                          case 'person':
                                                 li_data['media_type'] = '人物'
                                          case _:
                                                 li_data['media_type'] = '不明'
              data['results'].append(li_data)
       return data

