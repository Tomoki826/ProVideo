#!/home/tomoki826/anaconda3/bin/python3.9
from wsgiref.handlers import CGIHandler
from index import app

#if __name__=='__main__':
CGIHandler().run(app)