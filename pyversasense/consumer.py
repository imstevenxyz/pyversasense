import json
import requests

from .device import Device
from .peripheral import Peripheral
from .const import (ENDPOINT_DEVICES)

header = {'Content-Type': 'application/json'}

class Consumer:

    deviceList = []

    def __init__(self, host):
        self._host = host

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host(self, host):
        self._host = host

    def fetchPeripheralSample(self, peripheral):
        url = self._host + ENDPOINT_DEVICES + "/" + peripheral.parentMac + "/peripherals/" + peripheral.identifier + "/sample"
        response = requests.get(url, header)
        print(response)
        return response.json()

    def fetchDevices(self):
        self.deviceList.clear()
        url = self._host + ENDPOINT_DEVICES
        try:
            response = requests.get(url, header)
        except Exception as e:
            print(e)
            return False

        if response.status_code == 200:
            self._jsonToDeviceList(response.json())
            return True

        return False

    def _jsonToDeviceList(self, json):
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
            
            peripheralList = self._jsonToPeripheralList(peripherals, mac)

            self.deviceList.append(Device(address, peripheralList, name, description, location, type, battery, version, mac, status))

    def _jsonToPeripheralList(self, json, parentMac):
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