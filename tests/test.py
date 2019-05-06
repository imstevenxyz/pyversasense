import asynctest
import aiohttp
import asyncio
from pyversasense import Consumer

url = "https://107731e1-6ad3-4fac-937c-e115c6b5343f.mock.pstmn.io"
deviceMacs = ["00-17-0D-00-00-30-E9-A7", "00-17-0D-00-00-30-DC-5E", "00-17-0D-00-00-30-E9-62", "00-17-0D-00-00-30-DB-2B", "00-17-0D-00-00-58-BD-01"]
peripheralIds = ["8040/8042", "9803/9805", "1010/9000", "3303/5702"]
measurementNames = ["Temperature","Humidity","Light","Pressure","Battery capacity","Battery used","Battery level"]
samples = [41.18, 1765, 3000, 24.72, 43.45, 106.46, 1009.26]

class TestConsummer(asynctest.TestCase):
    async def setUp(self):
        async with aiohttp.ClientSession() as session:
            self.consumer = Consumer(url, session)
            self.deviceList = await self.consumer.fetchDevices()

    def test_host(self):
        host = self.consumer.host
        self.assertEqual(host, url)

    def test_device_mac(self):
        for device in self.deviceList:
            self.assertIn(device.mac, deviceMacs)

    def test_peripheral_id(self):
        for device in self.deviceList:
            for peripheral in device.peripherals:
                self.assertIn(peripheral.identifier, peripheralIds)
    
    def test_peripheral_measurements(self):
        for device in self.deviceList:
            for peripheral in device.peripherals:
                for measurement in peripheral.measurements:
                    self.assertIn(measurement.name, measurementNames)

    async def test_samples(self):
        async with aiohttp.ClientSession() as session:
            self.consumer = Consumer(url, session)
            self.deviceList = await self.consumer.fetchDevices()

            for device in self.deviceList:
                for peripheral in device.peripherals:
                    testsample = await self.consumer.fetchPeripheralSample(peripheral)
                    for sample in testsample:
                        self.assertIn(sample.value, samples)
            
            testcontrolesample = await self.consumer.fetchPeripheralSample(None, "3303/5702", "00-17-0D-00-00-30-E9-62")
            for sample in testcontrolesample:
                self.assertIn(sample.value, samples)

if __name__ == '__main__':
    asynctest.main()