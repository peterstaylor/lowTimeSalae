# import math
# import numpy

from saleae.range_measurements import DigitalMeasurer


class MyDigitalMeasurer(DigitalMeasurer):
    supported_measurements = []

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get transitions in the form of pairs of `Time`, Bitstate (`True` for high, `False` for low)
    # `Time` currently only allows taking a difference with another `Time`, to produce a `float` number of seconds
    lowTime = 0
    counting = False 
    startLow = 0
    endLow = 0
    lowSum = 0
    def process_data(self, data):
        for time, bitState in data: 
            if not bitState and not counting: 
                counting = True
                startLow = time
            else if bitState and counting: 
                counting = False
                endLow = time
                lowSum = lowSum + (endLow - startLow)
                startLow = 0
                endLow = 0
        pass

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {"lowTime": lowSum}
        return values
