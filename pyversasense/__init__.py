from .consumer import Consumer

def test():
    url = "https://107731e1-6ad3-4fac-937c-e115c6b5343f.mock.pstmn.io"
    #url = "https://gateway.versasense.com:8889"
    consumer = Consumer(url)
    consumer.fetchDevices()
    for d in consumer.deviceList:
        for per in d.peripherals:
            print(per.identifier)
            print(consumer.fetchPeripheralSample(per))

    return True