"""
Module for creating aiohttp web application and setup logger
"""
from typing import Dict

from aiohttp import web
from aiohttp.web_app import Application

from slb_task2.routes import setup_routes
import pandas as pd
import os
import logging
from functools import partial
import simplejson


def get_data():
    result = {}
    ia_df = pd.read_pickle(os.path.join(os.pardir, 'slb_data', 'ia_df.pkl'))
    result['ia_df'] = ia_df
    return result


async def create_app(config: Dict) -> Application:
    """
    Creating aiohttp web application

    :type config: Dict
    :rtype: Application
    :param config: application configuration dictionary
    :return:  aiohttp web application
    """
    app = web.Application()
    app['config'] = config

    setup_logger(config['log'], config['filelog'])
    app['data'] = get_data()
    app['dumps'] = partial(simplejson.dumps, ignore_nan=True)
    setup_routes(app)

    return app


def setup_logger(loglevel: str, filelog: bool) -> logging.Logger:
    numeric_level = getattr(logging, loglevel.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    logger = logging.getLogger()
    logger.setLevel(numeric_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if filelog:
        file_handler = logging.FileHandler('slb_task2-backend.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
