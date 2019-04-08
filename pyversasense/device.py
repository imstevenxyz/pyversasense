class Device:
    
    def __init__(self, address, peripherals, name, description, location, type, battery, version, mac, status):
        self._address = address
        self._peripherals = peripherals
        self._name = name
        self._description = description
        self._location = location
        self._type = type
        self._battery = battery
        self._version = version
        self._mac = mac
        self._status = status

    @property
    def address(self):
        return self._address
    
    @property
    def peripherals(self):
        return self._peripherals

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def location(self):
        return self._location

    @property
    def type(self):
        return self._type

    @property
    def battery(self):
        return self._battery

    @property
    def version(self):
        return self._version
        
    @property
    def mac(self):
        return self._mac

    @property
    def status(self):
        return self._status
