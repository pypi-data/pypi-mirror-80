# -*- coding: utf-8 -*-
import logging
import asyncio

from ..protocol import device, protocol
from ..exceptions import UnableToAuthenticate
_logger = logging.getLogger(__name__)

class Trackimo(object):

    def __init__(self, loop=None):
        super().__init__()
        self.__loop = loop if loop else asyncio.get_event_loop()

    async def login(self, clientid, clientsecret, username, password):
        self.__protocol = protocol.Protocol(clientid=clientid, clientsecret=clientsecret,username=username, password=password, loop=self.__loop)
        authData = await self.__protocol.login()
        if not authData:
            raise UnableToAuthenticate('Not authenticated with Trackimo API')

        deviceHandler = device.DeviceHandler(self.__protocol)
        self.devices = await deviceHandler.get()
        return self

    @property
    def auth(self):
        if not self.__protocol:
            _logger.error('Not currently connected. login() first.')
            return None
        return self.__protocol.auth