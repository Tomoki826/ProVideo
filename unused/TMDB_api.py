# import requests
import json

class TMDB:
    def __init__(self, token):
        self.token = token
        self.headers_ = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json;charset=utf-8'}
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'
        self.language = 'ja'
        self.region = 'JP'

    # URLを生成する
    def _json_by_get_request(self, url, params={}):
        params['language'] = self.language
        params['region'] = self.region
        res = requests.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)

    # キーワードに部分一致する映画タイトルを取得
    def search_movies(self, with_keywords, page):
        params = {'query': with_keywords}
        params['page'] = page
        url = f'{self.base_url_}search/movie'
        return self._json_by_get_request(url, params)

    # 映画情報を取得
    def get_movie(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}'
        return self._json_by_get_request(url)

    # 映画のプロバイダー情報を取得
    def get_movie_provider(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/watch/providers'
        return self._json_by_get_request(url)

    # 映画に対するユーザーの状態を取得
    def get_movie_account_states(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/account_states'
        return self._json_by_get_request(url)

    # 別言語の映画タイトルを取得
    def get_movie_alternative_titles(self, movie_id, country=None):
        url = f'{self.base_url_}movie/{movie_id}/alternative_titles'
        return self._json_by_get_request(url)

    # 日付期間内の映画情報の編集履歴を取得
    def get_movie_changes(self, movie_id, start_date=None, end_date=None):
        url = f'{self.base_url_}movie/{movie_id}'
        return self._json_by_get_request(url)

    # 映画の出演者・スタッフ全員を取得
    def get_movie_credits(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/credits'
        return self._json_by_get_request(url)

    # IMDBのID・SNSアカウントのIDを取得
    def get_movie_external_ids(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/external_ids'
        return self._json_by_get_request(url)

    # 映画ポスター・背景の画像パスを取得
    def get_movie_images(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/images'
        return self._json_by_get_request(url)

    # 映画のキーワードを取得
    def get_movie_keywords(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/keywords'
        return self._json_by_get_request(url)

    # 映画の公開日・DVD&Blu-rayリリース日を取得
    def get_movie_release_dates(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/release_dates'
        return self._json_by_get_request(url)

    # 映画の紹介映像を取得
    def get_movie_videos(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/videos'
        return self._json_by_get_request(url)

    # 映画の翻訳データを取得
    def get_movie_translations(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/translations'
        return self._json_by_get_request(url)

    # おすすめの映画情報を全て取得
    def get_movie_recommendations(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/recommendations'
        return self._json_by_get_request(url)

    # 似た映画の映画情報を全て取得
    def get_similar_movies(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/similar'
        return self._json_by_get_request(url)

    # 映画の評価情報を取得
    def get_movie_reviews(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/reviews'
        return self._json_by_get_request(url)

    # 映画リストを取得
    def get_movie_lists(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/lists'
        return self._json_by_get_request(url)

    # ランダムな映画情報を取得 (常に変化する)
    def get_latest_movies(self):
        url = f'{self.base_url_}movie/latest'
        return self._json_by_get_request(url)

    # 現在日本で上映中の映画情報を全て取得
    def get_now_playing_movies(self, page=None):
        url = f'{self.base_url_}movie/now_playing'
        return self._json_by_get_request(url)

    # 現在日本で人気な映画情報を全て取得
    def get_popular_movies(self, page=None):
        url = f'{self.base_url_}movie/popular'
        return self._json_by_get_request(url)

    # 日本で高評価な映画情報を全て取得
    def get_top_rated_movies(self, page=None):
        url = f'{self.base_url_}movie/top_rated'
        return self._json_by_get_request(url)

    # 近日公開予定の映画情報を全て取得
    def get_upcoming_movies(self, page=None):
        url = f'{self.base_url_}movie/upcoming'
        return self._json_by_get_request(url)