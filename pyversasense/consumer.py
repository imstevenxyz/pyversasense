import json
import asyncio
import aiohttp

from .jsonHelpers import jsonToSampleList, jsonToDeviceDict
from .const import (ENDPOINT_DEVICES, ENDPOINT_SAMPLE, ENDPOINT_ACTUATE, HEADER)

class Consumer:

    deviceList = []

    def __init__(self, host, webSession):
        self._host = host
        self._webSession = webSession

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self, host):
        self._host = host

    @property
    def webSession(self):
        return self._webSession
    
    @webSession.setter
    def webSession(self, webSession):
        self._webSession = webSession

    async def fetchPeripheralSample(self, peripheral=None, identifier=None, parentMac=None):
        """Get a sample for a peripheral."""
        url = self._host
        if peripheral is not None:
            url += ENDPOINT_SAMPLE.format(peripheral.parentMac, peripheral.identifier)
        elif identifier is not None and parentMac is not None:
            url += ENDPOINT_SAMPLE.format(parentMac, identifier)
        else:
            raise ValueError("Bad arguments")

        try:
            response = await _getRequest(self._webSession, url)
        except Exception as e:
            print(e)
            return None

        samples = jsonToSampleList(response)
        return samples

    async def actuatePeripheral(self, peripheral=None, identifier=None, parentMac=None, payload=None):
        """Actuate a peripheral."""
        url =  self._host
        if peripheral is not None:
            url += ENDPOINT_ACTUATE.format(peripheral.parentMac, peripheral.identifier)
        elif identifier is not None and parentMac is not None:
            url += ENDPOINT_ACTUATE.format(parentMac, identifier)
        else:
            raise ValueError("Bad arguments")

        try:
            response = await _putRequest(self._webSession, url, payload)
        except Exception as e:
            print(e)
            return None
        return response

    async def fetchDevices(self):
        """Get all devices from API and convert response to a list."""
        self.deviceList.clear()
        url = self._host + ENDPOINT_DEVICES

        try:
            response = await _getRequest(self._webSession, url)
        except Exception as e:
            print(e)
            return None

        self.deviceList =  jsonToDeviceDict(response)
        return self.deviceList

async def _getRequest(websession, url):
    """Send a GET request."""
    async with websession.get(url, headers=HEADER) as response:
        if response.status == 200:
            data = await response.json(content_type=None)
        else:
            raise Exception('Bad response status code: {}'.format(response.status))
    return data

async def _putRequest(websession, url, payload):
    print(url)
    async with websession.put(url, headers=HEADER, json=payload) as response:
        if response.status == 200:
            data = await response.json(content_type=None)
        else:
            raise Exception('Bad response status code: {}'.format(response.status))
    return data