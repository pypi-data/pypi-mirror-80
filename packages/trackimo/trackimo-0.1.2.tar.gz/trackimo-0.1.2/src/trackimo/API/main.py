# -*- coding: utf-8 -*-
import logging

from ..protocol import device, protocol
from ..exceptions import UnableToAuthenticate
_logger = logging.getLogger(__name__)

class Trackimo(object):

    async def login(self, clientid, clientsecret, username, password):
        self.__protocol = protocol.Protocol(clientid=clientid, clientsecret=clientsecret,username=username, password=password)
        authData = await self.__protocol.login()
        if not authData:
            raise UnableToAuthenticate('Not authenticated with Trackimo API')

        deviceHandler = device.DeviceHandler(self.__protocol)
        self.devices = await deviceHandler.get()