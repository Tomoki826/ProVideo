# 実行後、一番最初に実行する(コンストラクタみたいな)ファイルなので
# WEBアプリ全体に使用したい設定を作ると便利
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask構成開始
app = Flask(__name__)

# 設定ファイル
app.config.from_object('testapp.config')

# sqlite
db = SQLAlchemy(app)
from .models import employee

import testapp.views