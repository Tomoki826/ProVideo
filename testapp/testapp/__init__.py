from flask import Flask
#from test import bp

app = Flask(__name__)
app.config.from_object('testapp.config')


import testapp.views