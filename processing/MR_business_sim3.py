from mrjob.job import MRJob
import numpy as np


class MRBusinessSim2(MRJob):

    def mapper(self, _, line):
        bus_pair, count_pair = line.split('\t', 1)
        bus = eval(bus_pair)
        counts = eval(count_pair)
        yield bus, counts 

    def reducer(self, key, values):
        num = 0
        d0 = 0
        d1 = 0
        for counts in values:
            num += counts[0] * counts[1]
            d0 += counts[0] * counts[0]
            d1 += counts[1] * counts[1]
        yield key, float(num) / float(np.sqrt(d0) * np.sqrt(d1))

if __name__ == '__main__':
    MRBusinessSim2.run()
