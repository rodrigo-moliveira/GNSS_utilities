class TimeSeries:
    def __init__(self):
        self.timeSeriesDict = {}

    def addData(self, epoch, value):
        self.timeSeriesDict[epoch] = value

    def keys(self):
        return self.timeSeriesDict.keys()

    def values(self):
        return self.timeSeriesDict.values()

    def items(self):
        return self.timeSeriesDict.items()


class RinexClockContainer:
    """
    RinexClockContainer class

    Attributes
        ----------
        SatClocksDict : dict
            dictionary indexed by keys ['epoch', 'sat']. The corresponding value is the clock bias
        StationClocksDict : dict
            dictionary indexed by keys ['epoch', 'station']. The corresponding value is the clock bias
    """

    def __init__(self):
        self.SatClocksDict = {}  # dict: ['epoch','sat': value, ...]
        self.StationClocksDict = {}  # dict: ['epoch','station': value, ...]

    def addSatClock(self, sat, epoch, value):
        if sat not in self.SatClocksDict:
            self.SatClocksDict[sat] = TimeSeries()
        self.SatClocksDict[sat].addData(epoch, value)

    def addStationClock(self, station, epoch, value):
        if station not in self.StationClocksDict:
            self.StationClocksDict[station] = TimeSeries()
        self.StationClocksDict[station].addData(epoch, value)
