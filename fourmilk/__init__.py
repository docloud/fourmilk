# coding=utf8

import yaml
import logging
import logging.config
from flask import Flask

app = Flask(__name__)

try:
    config = yaml.load(open("app.yaml"))
except IOError:
    app.logger.info("Could not load environment config, use default.")
    config = {}

app.config.update(config)

if 'logging' in config:
    logging.config.dictConfig(config['logging'])
else:
    logging.basicConfig()
logger = logging.getLogger(__name__)
