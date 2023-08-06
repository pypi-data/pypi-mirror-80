# -*- coding: utf-8 -*-
"""
Device handler for Trackimo
"""

import logging
import sys
import os
from datetime import datetime, timedelta
from trackimo.errors import MissingInformation
import trackimo.protocol

_logger = logging.getLogger(__name__)

def listall(limit=20,page=1):
    return trackimo.protocol.api_get(f'accounts/{trackimo.protocol.TRACKIMO_ACCOUNTID}/devices?{limit},{page}')

def details(id):
    """Get device details

    Attributes:
        id (int): The device id
    """
    return trackimo.protocol.api_get(f'accounts/{trackimo.protocol.TRACKIMO_ACCOUNTID}/devices/{id}')

def location(id):
    """Get device location

    Attributes:
        id (int): The device id
    """
    return trackimo.protocol.api_get(f'accounts/{trackimo.protocol.TRACKIMO_ACCOUNTID}/devices/{id}/location')

def history(id, start_date=None, end_date=None, limit=20, page=1):
    """Get device history

    Attributes:
        id (int): The device id
        start_date (datetime): Starting date for the history
        end_date (datetime): End date for the history
        limit (int): Results per page
        page (int): Page number
    """
    if not start_date: start_date = datetime.now() - timedelta(hours=24)
    if not end_date: end_date = datetime.now()
    data = {
        "from": int(start_date.timestamp()),
        "to": int(end_date.timestamp()),
        "limit": limit,
        "page": page
    }
    return trackimo.protocol.api_get(f'accounts/{trackimo.protocol.TRACKIMO_ACCOUNTID}/devices/{id}/history', data)
