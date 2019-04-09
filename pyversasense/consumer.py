import json
import asyncio
import aiohttp

from .device import Device
from .peripheral import Peripheral
from .const import (ENDPOINT_DEVICES)

headers = {'Content-Type': 'application/json'}

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

    async def fetchPeripheralSample(self, peripheral):
        url = self._host + ENDPOINT_DEVICES + "/" + peripheral.parentMac + "/peripherals/" + peripheral.identifier + "/sample"
        try:
            response = await _webRequest(self._webSession, url)
        except Exception as e:
            print(e)
            return False
        return response

    async def fetchDevices(self):
        self.deviceList.clear()
        url = self._host + ENDPOINT_DEVICES
        try:
            response = await _webRequest(self._webSession, url)
        except Exception as e:
            print(e)
            return False
        self.deviceList =  _jsonToDeviceList(response)
        return self.deviceList

async def _webRequest(websession, url):
    async with websession.get(url, headers=headers) as response:
        print(response.status)
        if response.status == 200:
            data = await response.json(content_type=None)
        else:
            raise Exception('Bad response status code: {}'.format(response.status))
    return data

def _jsonToDeviceList(json):
    deviceList = []
    for jsonDevice in json:
        address = jsonDevice["address"]
        peripherals = jsonDevice["peripherals"]
        name = jsonDevice["name"]
        description = jsonDevice["description"]
        location = jsonDevice["location"]
        type = jsonDevice["type"]
        battery = jsonDevice["battery"]
        version =jsonDevice["version"]
        mac = jsonDevice["mac"]
        status = jsonDevice["status"]
        peripheralList = _jsonToPeripheralList(peripherals, mac)
        deviceList.append(Device(address, peripheralList, name, description, location, type, battery, version, mac, status))
    return deviceList

def _jsonToPeripheralList(json, parentMac):
    peripheralList =  []
    for peripheral in json:
        samplingRate = peripheral["sampling_rate"]
        identifier = peripheral["identifier"]
        lastUpdated = peripheral["last_updated"]
        color = peripheral["color"]
        icon = peripheral["icon"]
        text = peripheral["text"]
        classification = peripheral["class"]
        peripheralList.append(Peripheral(samplingRate, identifier, lastUpdated, color, icon, text, classification, parentMac))
    return peripheralList