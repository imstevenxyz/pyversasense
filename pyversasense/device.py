class Device:
    
    def __init__(self, name, status, mac, address, peripherals):
        self._name = name
        self._status = status
        self._mac = mac
        self._address = address
        self._peripherals = peripherals

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def mac(self):
        return self._mac

    @property
    def address(self):
        return self._address
    
    @property
    def peripherals(self):
        return self._peripherals

    @name.setter
    def name(self, name):
        self._name = name

    @status.setter
    def status(self, status):
        self._status = status

    @mac.setter
    def mac(self, mac):
        self._mac = mac

    @address.setter
    def address(self, address):
        self._address = address

    @peripherals.setter
    def peripherals(self, peripherals):
        self._peripherals = peripherals


