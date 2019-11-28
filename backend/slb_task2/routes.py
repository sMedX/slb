"""
Module to setup handlers for processing REST API requests from front-end and enabling CORS
"""
from aiohttp.web_app import Application

from slb_task2 import handlers
import aiohttp_cors
import os
import logging

log = logging.getLogger(__name__)


def setup_routes(app: Application) -> None:
    """
    Setup handlers for processing requests from front-end and enable CORS

    :param app: aiohttp async web application
    """
    app.router.add_get("/attributes", handlers.get_attributes_handler)
    app.router.add_post("/filter_packers", handlers.filter_packers_by_ied_handler)

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)
