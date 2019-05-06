import json
import asyncio
import aiohttp

from .device import Device
from .peripheral import Peripheral
from .sample import Sample
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
        """Get a sample for a peripheral."""
        url = self._host + ENDPOINT_DEVICES + "/" + peripheral.parentMac + "/peripherals/" + peripheral.identifier + "/sample"
        try:
            response = await _webRequest(self._webSession, url)
        except Exception as e:
            print(e)
            return False
        samples = _jsonToSampleList(response)
        return samples

    async def fetchDevices(self):
        """Get all devices from API and convert response to a list."""
        self.deviceList.clear()
        url = self._host + ENDPOINT_DEVICES
        try:
            response = await _webRequest(self._webSession, url)
        except Exception as e:
            print(e)
            return False
        self.deviceList =  _jsonToDeviceList(response)
        return self.deviceList

def _jsonToDeviceList(json):
    """Convert json to list of Device objects."""
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
    """Convert json to list of Peripheral objects."""
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

def _jsonToSampleList(json):
    """Convert json to list of Sample objects"""
    sampleList = []
    parentId = json["identifier"]
    for data in json["data"]:
        unit = data["unit"]
        value = data["value"]
        datatype = data["datatype"]
        measurement = data["measurement"]
        timestamp = data["timestamp"]
        sampleList.append(Sample(unit, value, datatype, measurement, timestamp, parentId))
    return sampleList

async def _webRequest(websession, url):
    """Send a webrequest."""
    async with websession.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json(content_type=None)
        else:
            raise Exception('Bad response status code: {}'.format(response.status))
    return data