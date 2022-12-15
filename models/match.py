from models.TMDB import TMDB
from models.config import SENSITIVE_SEARCH

# idと一致する検索結果を探す
def match_work_id(id, name, media_type="Unknown", api_key=""):
       if media_type == "unknown" : return None
       page = 1
       while True:
              if media_type == "movie":
                     soup = TMDB(api_key).search_movies(name, page, SENSITIVE_SEARCH)
              elif media_type == "tv":
                     soup = TMDB(api_key).search_tvshows(name, page, SENSITIVE_SEARCH)
              elif media_type == "person":
                     soup = TMDB(api_key).search_person(name, page, SENSITIVE_SEARCH)
              if soup.get("results", []) == []: return None
              for item in soup["results"]:
                     if item['id'] == id:
                            item['media_type'] = media_type
                            return item
              page += 1