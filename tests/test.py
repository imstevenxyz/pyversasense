import asynctest
import aiohttp
import asyncio
from pyversasense import Consumer

url = "http://localhost:3000"
deviceMacs = ["00-17-0D-00-00-30-E9-A7", "00-17-0D-00-00-30-DC-5E", "00-17-0D-00-00-30-E9-62", "00-17-0D-00-00-30-DB-2B", "00-17-0D-00-00-58-BD-01"]
peripheralIds = ["8040/8042", "9803/9805", "1010/9000", "3303/5702", "3338/5850", "3302/5500"]
measurementNames = ["Temperature","Humidity","Light","Pressure","Battery capacity","Battery used","Battery level",'Buzzer','Motion','Motion Numeric']
samples = [41.18, 1765, 3000, 24.72, 43.45, 106.46, 1009.26, "OFF", "DETECTED", 1]

class TestConsummer(asynctest.TestCase):
    async def setUp(self):
        async with aiohttp.ClientSession() as session:
            self.consumer = Consumer(url, session)
            self.deviceList = await self.consumer.fetchDevices()

    def test_host(self):
        host = self.consumer.host
        self.assertEqual(host, url)

    def test_device_mac(self):
        for mac, device in self.deviceList.items():
            self.assertEqual(mac, device.mac)
            self.assertIn(device.mac, deviceMacs)

    def test_peripheral_id(self):
        for mac, device in self.deviceList.items():
            self.assertEqual(mac, device.mac)
            for id, peripheral in device.peripherals.items():
                self.assertEqual(id, peripheral.identifier)
                self.assertIn(peripheral.identifier, peripheralIds)
    
    def test_peripheral_measurements(self):
        for mac, device in self.deviceList.items():
            self.assertEqual(mac, device.mac)
            for id, peripheral in device.peripherals.items():
                self.assertEqual(id, peripheral.identifier)
                for measurement in peripheral.measurements:
                    self.assertIn(measurement.name, measurementNames)

    async def test_samples(self):
        async with aiohttp.ClientSession() as session:
            self.consumer = Consumer(url, session)
            self.deviceList = await self.consumer.fetchDevices()

            for mac, device in self.deviceList.items():
                self.assertEqual(mac, device.mac)
                for id, peripheral in device.peripherals.items():
                    self.assertEqual(id, peripheral.identifier)
                    testsample = await self.consumer.fetchPeripheralSample(peripheral)
                    for sample in testsample:
                        self.assertIn(sample.value, samples)
            
            testcontrolesample = await self.consumer.fetchPeripheralSample(None, "3303/5702", "00-17-0D-00-00-30-E9-62")
            for sample in testcontrolesample:
                self.assertIn(sample.value, samples)

    async def test_peripheral_actuation(self):
        async with aiohttp.ClientSession() as session:
            self.consumer = Consumer(url, session)
            self.deviceList = await self.consumer.fetchDevices()
            
            data = { "id": "state-num", "value": 1}
            response = await self.consumer.actuatePeripheral(None, "3338/5850", "00-17-0D-00-00-30-E9-62", data)
            print(response)

if __name__ == '__main__':
    asynctest.main()