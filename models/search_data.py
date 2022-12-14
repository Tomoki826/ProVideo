from models.enum import Search
from models.genre import Genre
from models.config import SENSITIVE_SEARCH
from models.kanji import Japanese_check
import re, datetime

# 検索情報をフォーマットする
class Search_Data:

       # 初期設定
       def __init__(self, raw_data):
              self.data = {}
              self.raw_data = raw_data

       # 情報をフォーマット
       def search_arrange(self, search_type=Search.MULTI, page=1, keywords=''):
              self.data['keywords'] = keywords
              self.data['current_page'] = page
              if self.raw_data.get('total_results') != None:
                     self.data['max_page'] = (self.raw_data['total_results'] - 1) // 20 + 1
                     self.data['total_results'] = self.raw_data['total_results']
              # 検索タイプ
              self.data['search_type'] = int(search_type)
              if search_type == Search.MOVIES or search_type == Search.TVSHOWS or search_type == Search.MULTI or search_type == Search.PERSON:
                     self.data['search_type-btn'] = int(search_type)
              else:
                     self.data['search_type-btn'] = int(Search.MULTI)
              # 検索データの整理
              self.data['results'] = []
              for item in self.raw_data['results']:
                     if self.data['search_type'] == Search.PERSON or self.data['search_type'] == Search.DISCOVER_PERSON or item.get('media_type') == 'person':
                            data = self.__person_results_type__(item)
                     elif item.get('media_type') == 'text' or item.get('media_type') == 'pv' or item.get('media_type') == 'image':
                            data = self.__feature_type__(item)
                     else:
                            data = self.__video_type__(item)
                     self.data['results'].append(data)
              return self.data

       # 作品データを修正
       def __video_type__(self, item):
              data = {}
              # id
              data['id'] = item['id']
              # 作品タイトル
              if 'adult' not in item:
                     data['adult'] = 'false'
              if 'title' in item:
                     data['title'] = item['title'].strip()
              elif 'name' in item:
                     data['title'] = item['name'].strip()
              elif 'original_title' in item:
                     data['title'] = item['original_title'].strip()
              elif 'original_name' in item:
                     data['title'] = item['original_name'].strip()
              else:
                     data['title'] = '(タイトル情報なし)'
              # 公開日
              if 'release_date' in item:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['release_date']):
                            dte = datetime.datetime.strptime(item['release_date'], '%Y-%m-%d')
                            data['openday'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
              elif 'first_air_date' in item:
                     # 日付文字列の正規表現パターンと一致するか確認
                     if re.fullmatch(r'\d{4}-\d{2}-\d{2}', item['first_air_date']):
                            dte = datetime.datetime.strptime(item['first_air_date'], '%Y-%m-%d')
                            data['openday'] = '公開日: ' + str(dte.year) + '年' + str(dte.month) + '月' + str(dte.day) + '日'
              if 'openday' not in data:
                     data['openday'] = '公開日: 不明'
              # ジャンル
              if 'genres' in item:
                     data['genre'] = 'ジャンル: '
                     for genre in item['genres']:
                            data['genre'] += Genre().name_get(genre.get('id')) + ', '
                     data['genre'] = data['genre'][:-2]
              elif 'genre_ids' not in item or item.get('genre_ids') == []:
                     data['genre'] = 'ジャンル: 不明'
              else:
                     data['genre'] = 'ジャンル: '
                     for id in item['genre_ids']:
                             data['genre'] += Genre().name_get(id) + ', '
                     data['genre'] = data['genre'][:-2]
              # 注目度
              data['popularity'] = item.get('popularity', 0)
              # ポスター画像
              data['poster_path'] = item.get('poster_path', '')
              # 識別子
              data['media_type'] = item.get('media_type', 'Unknown')
              # メディアタイプ
              if item.get('adult') == True:
                     data['data_type'] = 'sensitive'
                     data['print_type'] = 'センシティブ'
              else:
                     if self.data['search_type'] == Search.MOVIES or self.data['search_type'] == Search.DISCOVER_MOVIE:
                            data['data_type'] = 'movie'
                            data['print_type'] = '映画'
                     elif self.data['search_type'] == Search.TVSHOWS:
                            if SENSITIVE_SEARCH == False:
                                   data['data_type'] = 'tv'
                            else:
                                   data['data_type'] = 'tv-sensitive'
                            data['print_type'] = 'テレビ・配信番組'
                     elif self.data['search_type'] == Search.DISCOVER_TV:
                            data['data_type'] = 'tv'
                            data['print_type'] = 'テレビ・配信番組'
                     elif self.data['search_type'] == Search.MULTI:
                            if 'media_type' not in item:
                                   data['data_type'] = 'Unknown'
                                   data['print_type'] = '不明'
                            else:
                                   if item['media_type'] == 'movie':
                                          data['data_type'] = 'movie'
                                          data['print_type'] = '映画'
                                   elif item['media_type'] == 'tv':
                                          if SENSITIVE_SEARCH == False:
                                                 data['data_type'] = 'tv'
                                          else:
                                                 data['data_type'] = 'tv-sensitive'
                                          data['print_type'] = 'テレビ・配信番組'
                                   else:
                                          data['data_type'] = 'Unknown'
                                          data['print_type'] = '不明'
              # あらすじ
              if len(item.get('overview', '')) >= 1:
                     data['overview'] = item.get('overview')
              else:
                     data['overview'] = "情報なし"
              return data           


       # 人物データを修正
       def __person_results_type__(self, item):
              data = {}
              # 名前
              data['title'] = item['name'].strip()
              if Japanese_check([item['name'].strip()]) != '':
                     data['JP_name'] = True
              else:
                     data['JP_name'] = False
              #id
              data['id'] = item['id']
              # 職業
              job = item.get('known_for_department')
              if job == "Acting":
                     data['known_videos'] = "主な出演作品"
                     gender = item.get('gender')
                     if gender == 1:
                            data['department'] = "職業: タレント・女優"
                     elif gender == 2:
                            data['department'] = "職業: タレント・俳優"
                     else:
                            data['department'] = "職業: タレント"
              elif job == "Production":
                     data['known_videos'] = "主な作品"
                     data['department'] = "職業: プロデューサー"
              elif job == "Visual Effects":
                     data['known_videos'] = "主な作品"
                     data['department'] = "職業: エフェクト・CGクリエイター"
              elif job == "Directing":
                     data['known_videos'] = "主な作品"
                     data['department'] = "職業: ディレクター・監督"
              elif job == "Sound":
                     data['known_videos'] = "主な作品"
                     data['department'] = "職業: ミュージシャン"
              elif job == "Writing":
                     data['known_videos'] = "主な作品"
                     data['department'] = "職業: 作家・ライター"
              elif job == "Editing":
                     data['known_videos'] = "主な作品"
                     data['department'] = "職業: 映像クリエイター"
              elif job == "Art":
                     data['known_videos'] = "主な作品"
                     data['department'] = "職業: デザイナー"
              else:
                     data['known_videos'] = "主な作品"
                     data['department'] = "職業: 不明"
              # 性別
              if item.get('gender') == 1:
                     data['gender'] = "性別: 女性"
              elif item.get('gender') == 2:
                     data['gender'] = "性別: 男性"
              else:
                     data['gender'] = "性別: その他・不明"
              # 注目度
              data['popularity'] = item.get('popularity', 0)
              # ポスター画像
              data['poster_path'] = item.get('profile_path', '')
              # 出演作
              data['known_for'] = []
              if 'known_for' in item:
                     for item2 in item['known_for']:
                            li = {}
                            # ポスター画像
                            if 'poster_path' in item2 and (item2.get('adult') != True or (item2.get('adult') == True and SENSITIVE_SEARCH == True)):
                                   li['poster_path'] = item2['poster_path']
                            else:
                                   continue
                            # id
                            li['id'] = item2['id']
                            # タイトル
                            if 'title' in item2:
                                   li['title'] = item2['title'].strip()
                            elif 'name' in item2:
                                   li['title'] = item2['name'].strip()
                            elif 'original_title' in item2:
                                   li['title'] = item2['original_title'].strip()
                            elif 'original_name' in item2:
                                   li['title'] = item2['original_name'].strip()
                            else:
                                   li['title'] = '(タイトル情報なし)'
                            data['known_for'].append(li)
              # 識別子
              data['media_type'] = 'person'
              # メディアタイプ
              if item.get('adult') == True:
                     data['data_type'] = 'sensitive'
                     data['print_type'] = 'センシティブ'
              else:
                     data['data_type'] = 'person'
                     data['print_type'] = '人物'
              return data

       # その他のメディアタイプを修正
       def __feature_type__(self, item):
              item['data_type'] = item['media_type']
              # テキスト部分を修正
              if item['media_type'] == "text":
                     if item.get('title') == None:
                            item['title'] = ""
                     if item.get('link') == None:
                            item['link'] = []
              if item['media_type'] == "image":
                     if item.get('text') == None:
                            item['text'] = ""
                     if item.get('link') == None:
                            item['link'] = []
              return item