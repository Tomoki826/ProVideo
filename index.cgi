#!/home/tomoki826/anaconda3/bin/python3.9
from wsgiref.handlers import CGIHandler
from run import app

#if __name__=='__main__':
CGIHandler().run(app)