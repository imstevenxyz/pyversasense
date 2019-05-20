from .device import Device
from .peripheral import Peripheral
from .sample import Sample
from .measurement import Measurement

def jsonToDeviceDict(json):
    """Convert json to list of Device objects."""
    deviceDict = {}
    for jsonDevice in json:
        mac = jsonDevice.get("mac")
        address = jsonDevice.get("address")
        name = jsonDevice.get("name")
        description = jsonDevice.get("description")
        location = jsonDevice.get("location")
        type = jsonDevice.get("type")
        battery = jsonDevice.get("battery")
        version =jsonDevice.get("version")
        status = jsonDevice.get("status")

        peripherals = jsonDevice.get("peripherals")
        peripheralList = jsonToPeripheralDict(peripherals, mac)

        deviceDict.update({mac : Device(address, peripheralList, name, description, location, type, battery, version, mac, status)})
    return deviceDict

def jsonToPeripheralDict(json, parentMac):
    """Convert json to list of Peripheral objects."""
    peripheralDict =  {}
    for peripheral in json:
        identifier = peripheral.get("identifier")
        samplingRate = peripheral.get("sampling_rate")
        lastUpdated = peripheral.get("last_updated")
        color = peripheral.get("color")
        icon = peripheral.get("icon")
        text = peripheral.get("text")
        classification = peripheral.get("class")

        measurements = peripheral.get("measurements")
        measurementList = jsonToMeasurementList(measurements)

        peripheralDict.update({ identifier : Peripheral(samplingRate, identifier, lastUpdated, color, icon, text, classification, parentMac, measurementList)})
    return peripheralDict

def jsonToMeasurementList(json):
    """Convert json to list of measurements"""
    measurementList = []
    for measurement in json:
        unit = measurement.get("unit")
        rounding = measurement.get("round")
        datatype = measurement.get("datatype")
        origin = measurement.get("origin")
        decimals = measurement.get("decimals")
        name = measurement.get("name")
        formula = measurement.get("formula")

        measurementList.append(Measurement(unit, rounding, datatype, origin, decimals, name, formula))
    return measurementList

def jsonToSampleList(json):
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