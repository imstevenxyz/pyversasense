import asyncio
import aiohttp

from .consumer import Consumer

url = "https://gateway.versasense.com:8889"

async def main(url):
    async with aiohttp.ClientSession() as session:
        consumer = Consumer(url, session)
        await consumer.fetchDevices()
        for d in consumer.deviceList:
            for per in d.peripherals:
                print(per.identifier)
                sample = await consumer.fetchPeripheralSample(per)
                print(sample)

    return True

def test(url = url):
    asyncio.get_event_loop().run_until_complete(main(url))