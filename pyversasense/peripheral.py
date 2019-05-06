class Peripheral:
    """Representation of a peripheral, e.g. sensor."""
    
    def __init__(self, samplingRate, identifier, lastUpdated, color, icon, text, classification, parentMac, measurements):
        self._samplingRate = samplingRate
        self._identifier = identifier
        self._lastUpdated = lastUpdated
        self._color = color
        self._icon = icon
        self._text = text
        self._classification = classification
        self._parentMac = parentMac
        self._measurements = measurements

    @property
    def samplingRate(self):
        return self._samplingRate
    
    @property
    def identifier(self):
        return self._identifier

    @property
    def lastUpdated(self):
        return self._lastUpdated
    
    @property
    def color(self):
        return self._color

    @property
    def icon(self):
        return self._icon
    
    @property
    def text(self):
        return self._text

    @property
    def classification(self):
        return self._classification

    @property
    def parentMac(self):
        return self._parentMac

    @property
    def measurements(self):
        return self._measurements