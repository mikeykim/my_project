import requests
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup

from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client.dbsparta
collection = db.collection
docs = collection.find({})
weekno = datetime.datetime.today().weekday()


def update():
    players = list(db.myfantasystar.find({}, {'_id': False}, {'position': False}, {'match': False}, {'goal': False},
                                         {'assi': False}, {'img_url': False}).sort('name', ))
    if weekno == 2:
        players['like'] = '0'
        players['pre_like'] = '0'
    else:
        players['pre_like'] = players['like']
        players['like'] = '0'

    print(players)


    # like_info = {
    #     'like': players['pre_like'],
    #     'pre_like': players['like'],
    # }
    # db.likedb.insert_one(like_info)

#
# def like_reset():
#     like = list(db.myfantasystar.find({}, {'_id': False}).sort('name', ))
#     pre_like =
#     if weekno == 2:
#         like = '0'
#         pre_like = '0'
#
# #오잉?! like를 0으로 선언했기 때문에 like를 바로 넣으면 안될듯?
#
# def like_update():
#     if weekno != 2:
#         pre_like = 'like'
#         like = '0'
