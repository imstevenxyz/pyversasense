class Measurement:

    def __init__(self, unit, rounding, datatype, origin, decimals, name, formula):
        self._unit = unit
        self._rounding = rounding
        self._datatype = datatype
        self._origin = origin
        self._decimals = decimals
        self._name = name
        self._formula = formula

    @property
    def unit(self):
        return self._unit

    @property
    def rounding(self):
        return self._rounding

    @property
    def datatype(self):
        return self._datatype

    @property
    def origin(self):
        return self._origin

    @property
    def decimals(self):
        return self._decimals

    @property
    def name(self):
        return self._name

    @property
    def formula(self):
        return self._formula