# coding=utf8

import pymongo
from fourmilk import config, logger

try:
    mongo_client = pymongo.MongoClient(config['mongodb']['host'],
                                       config['mongodb']['port'])
    mongo = mongo_client.fourmilk
except:
    logger.warn("Could not connected MongoDB.")
    mongo = None
