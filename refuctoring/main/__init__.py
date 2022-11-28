# 実行後、一番最初に実行する(コンストラクタみたいな)ファイルなので
# WEBアプリ全体に使用したい設定を作ると便利
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask構成開始
app = Flask(__name__)

# 設定ファイル
app.config.from_object('main.models.config')

# モジュールを導入
"""
from testapp.test import test_module
app.register_blueprint(test_module)
from testapp.janken import janken_module
app.register_blueprint(janken_module)
"""

# SQLを設定
db = SQLAlchemy(app)
from main.models.database import Users

import os;
if os.path.exists('./instance/database.db') == False:
    with app.app_context():
        db.drop_all()
        db.create_all()

# APIの環境変数が存在するか？
# (APIキーのテンプレート・取得方法は".env.sample"を参照)
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
api_key = os.environ.get("API_KEY")
if not api_key:
    raise RuntimeError("API_KEY not set")

# views.pyの内容を読み込み(ホームページ)
import main.models.index