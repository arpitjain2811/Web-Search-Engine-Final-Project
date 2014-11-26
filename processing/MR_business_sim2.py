from mrjob.job import MRJob
from itertools import combinations


class MRBusinessSim2(MRJob):

    def mapper(self, _, line):
        word, values = line.split('\t', 1)
        pair = eval(values)
        yield word.strip('"'), pair 

    def reducer(self, key, values):
        for pair in combinations(values, 2):
            if pair[0][0] < pair[1][0]:
                yield (pair[0][0], pair[1][0]), (pair[0][1], pair[1][1])
            elif pair[0][0] > pair[1][0]:
                yield (pair[1][0], pair[0][0]), (pair[1][1], pair[0][1])
            else:
                pass

if __name__ == '__main__':
    MRBusinessSim2.run()
