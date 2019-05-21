# VersaSense API consumer

A Python library to communicate with the VersaSense API.

## Getting Started

### Dependencies

- aiohttp
- asyncio

### Installation

```
pip install pyversasense
```

### Basic Usage

```python
import asyncio
import aiohttp
import pyversasense as pyv

url = "https://gateway.versasense.com:8889"

async def example():
    async with aiohttp.ClientSession() as session:
        consumer = pyv.Consumer(url, session)
        devices = await consumer.fetchDevices()

        for mac, device in devices.items():
            print("Mac: {} Name: {}".format(mac, device.name))

asyncio.get_event_loop().run_until_complete(example()) 
```
