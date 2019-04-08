import json
import requests

from .device import Device
from .peripheral import Peripheral
from .const import (ENDPOINT_DEVICES)

header = {'Content-Type': 'application/json'}
deviceList = []

class Consumer:

    def __init__(self, host):
        self._host = host

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self, host):
        self._host = host

    def fetchPeripheralSample(self, mac, identifier):
        url = self._host + ENDPOINT_DEVICES + "/" + mac + "/peripherals/" + identifier + "/sample"
        print(url)
        response = requests.get(url, header)
        return response.json()

    def fetchDevices(self):
        deviceList.clear()
        url = self._host + ENDPOINT_DEVICES
        response = requests.get(url, header)
        #todo check response code
        for jsonDevice in response.json():
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

            peripheralList = self._jsonToPeripheralList(peripherals, mac)

            deviceList.append(Device(address, peripheralList, name, description, location, type, battery, version, mac, status))

        return True

    def _jsonToPeripheralList(self, json, deviceMac):
        peripheralList =  []
        for peripheral in json:
            samplingRate = peripheral["sampling_rate"]
            identifier = peripheral["identifier"]
            lastUpdated = peripheral["last_updated"]
            color = peripheral["color"]
            icon = peripheral["icon"]
            text = peripheral["text"]
            classification = peripheral["class"]
            peripheralList.append(Peripheral(samplingRate, identifier, lastUpdated, color, icon, text, classification, deviceMac))
        return peripheralList

def test():
    url = "https://e0464716-c94d-47b9-867a-c297d6caa1d2.mock.pstmn.io"
    consumer = Consumer(url)
    consumer.fetchDevices()
    for d in deviceList:
        for per in d.peripherals:
            print(per.identifier)
            print(per.getSample(consumer))

    return True