# アプリの設定ファイル
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///sample_flask.db'

# データベースのイベントシステムがセッションの変更を追跡
# (リソース節約のためにオフでもよい)
SQLALCHEMY_TRACK_MODIFICATIONS = True
