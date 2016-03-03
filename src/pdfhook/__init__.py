# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint(
    'pdfhook', __name__,
)

from . import views
