import enum

# 列挙型の一覧
class Search(enum.IntEnum):
    MOVIES = 1
    TVSHOWS = 2
    MULTI = 3
    PERSON = 4
    DISCOVER_MOVIE = 5
    DISCOVER_TV = 6