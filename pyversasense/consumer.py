import json
import asyncio
import aiohttp

from .device import Device
from .peripheral import Peripheral
from .sample import Sample
from .measurement import Measurement
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

    async def fetchPeripheralSample(self, peripheral=None, identifier=None, parentMac=None):
        """Get a sample for a peripheral."""
        if peripheral is not None:
            url = self._host + ENDPOINT_DEVICES + "/" + peripheral.parentMac + "/peripherals/" + peripheral.identifier + "/sample"
        elif identifier is not None and parentMac is not None:
            url = self._host + ENDPOINT_DEVICES + "/" + parentMac + "/peripherals/" + identifier + "/sample"
        else:
            raise ValueError("Bad arguments")

        try:
            response = await _webRequest(self._webSession, url)
        except Exception as e:
            print(e)
            return None

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
            return None

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
        measurements = peripheral["measurements"]
        measurementList = _jsonToMeasurementList(measurements)
        peripheralList.append(Peripheral(samplingRate, identifier, lastUpdated, color, icon, text, classification, parentMac, measurementList))
    return peripheralList

def _jsonToMeasurementList(json):
    """Convert json to list of measurements"""
    measurementList = []
    for measurement in json:
        unit = measurement["unit"]
        rounding = measurement["round"]
        datatype = measurement["datatype"]
        origin = measurement["origin"]
        decimals = measurement["decimals"]
        name = measurement["name"]
        formula = measurement["formula"]
        measurementList.append(Measurement(unit, rounding, datatype, origin, decimals, name, formula))
    return measurementList

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
    """Send a GET request."""
    async with websession.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json(content_type=None)
        else:
            raise Exception('Bad response status code: {}'.format(response.status))
    return data