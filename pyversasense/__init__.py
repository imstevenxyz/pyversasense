import json
import requests

from .device import Device
from .const import (ENDPOINT_DEVICES)

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

    def fetchDevices(self):
        header = {'Content-Type': 'application/json'}
        url = self._host + ENDPOINT_DEVICES

        response = requests.get(url, header)
        print(response)
        print(response.json())

        for jsonDevice in response.json():
            name = jsonDevice["name"]
            status = jsonDevice["status"]
            mac = jsonDevice["mac"]
            address = jsonDevice["address"]
            peripherals = jsonDevice["peripherals"]

            deviceList.append(Device(name, status, mac, address, peripherals))

        for d in deviceList:
            print(d.name)

        return True