import requests
import json

class TMDB:
    def __init__(self, token):
        self.token = token
        self.headers_ = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json;charset=utf-8'}
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'
    
    # URLを生成する
    def _json_by_get_request(self, url, params={}):
        params['language'] = "ja"
        params['region'] = "JP"
        res = requests.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)
    
    # キーワードに部分一致する映画タイトルを取得
    def search_movies(self, with_keywords, page, adult=False):
        params = {
            'query': with_keywords,
            'page': page,
            'language': "ja",
            'region': "JP",
        }
        if adult:
            params['include_adult'] = 'true'
        else:
            params['include_adult'] = 'false'
        url = f'{self.base_url_}search/movie'
        return self._json_by_get_request(url, params)

    # キーワードに部分一致するテレビ番組を取得
    def search_tvshows(self, with_keywords, page, adult=False):
        params = {
            'query': with_keywords,
            'page': page,
            'language': "ja",
            'region': "JP",
        }
        if adult:
            params['include_adult'] = 'true'
        else:
            params['include_adult'] = 'false'
        url = f'{self.base_url_}search/tv'
        return self._json_by_get_request(url, params)

    # キーワードに部分一致するテレビ番組・映画・人物をまとめて取得
    def search_multi(self, with_keywords, page, adult=False):
        params = {
            'query': with_keywords,
            'page': page,
            'language': "ja",
            'region': "JP",
        }
        if adult:
            params['include_adult'] = 'true'
        else:
            params['include_adult'] = 'false'
        url = f'{self.base_url_}search/multi'
        return self._json_by_get_request(url, params)
    
    # キーワードに一致する人物を取得
    def search_person(self, with_keywords, page, adult=False):
        params = {
            'query': with_keywords,
            'page': page,
            'language': "ja",
            'region': "JP",
        }
        if adult:
            params['include_adult'] = 'true'
        else:
            params['include_adult'] = 'false'
        url = f'{self.base_url_}search/person'
        return self._json_by_get_request(url, params)

    # 注目の映画を取得
    def discover_movie(self, page):
        params = {
            'page': page,
            'watch_region': 'JP',
            'with_release_type': 4,
            'with_watch_monetization_types': 'flatrate',
            'language': "ja",
            'region': "JP",
        }
        url = f'{self.base_url_}discover/movie'
        return self._json_by_get_request(url, params)
    
    # 注目のテレビ・配信番組を取得
    def discover_tvshows(self, page):
        params = {
            'page': page,
            'watch_region': 'JP',
            'with_release_type': 4,
            'with_watch_monetization_types': 'flatrate',
            'language': "ja",
            'region': "JP",
        }
        url = f'{self.base_url_}discover/tv'
        return self._json_by_get_request(url, params)

    # 注目の人物を取得
    def discover_person(self, page):
        params = {
            'page': page,
            'watch_region': 'JP',
            'with_release_type': 4,
            'with_watch_monetization_types': 'flatrate',
            'language': "ja",
            'region': "JP",
        }
        url = f'{self.base_url_}person/popular'
        return self._json_by_get_request(url, params)
    
    # 人物の日本語訳を取得
    def person_id(self, id):
        params = {
            'language': "ja",
            'region': "JP",
        }
        url = f'{self.base_url_}person/{id}'
        return self._json_by_get_request(url, params)
    
    # プロバイダー情報を取得
    def get_provider_info(self, id, data_type):
        params = {
            'language': "ja",
            'region': "JP",
        }
        if data_type == "movie":
            return self._json_by_get_request(f'{self.base_url_}movie/{id}/watch/providers', params)
        elif data_type == "tv":
            return self._json_by_get_request(f'{self.base_url_}tv/{id}/watch/providers', params)
        return {}
    
    # 作品の詳細情報を取得
    def get_detail_info(self, id, data_type):
        if data_type == "movie":
            return self._json_by_get_request(f'{self.base_url_}movie/{id}')
        elif data_type == "tv":
            return self._json_by_get_request(f'{self.base_url_}tv/{id}')
        elif data_type == "person":
            return self._json_by_get_request(f'{self.base_url_}person/{id}')
        return {}

    # プロバイダーの映画・配信番組を取得
    def get_providers_works(self, id, page, data_type, japanese):
        params = {
            'page': page,
            'watch_region': 'JP',
            'with_watch_providers': id,
        }
        if japanese:
            params['language'] = "ja"
            params['region'] = "JP"
        url = f'{self.base_url_}discover/{data_type}'
        return self._json_by_get_request(url, params)
