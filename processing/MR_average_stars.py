from mrjob.job import MRJob
import json

class MRAvgReview(MRJob):

    def mapper(self, _, line):
        obj = json.loads(line)
        yield obj['business_id'], obj['stars']

    def reducer(self, key, values):
        count = 0
        total = 0
        for v in values:
            total += v
            count += 1
        yield key, float(total) / count

if __name__ == '__main__':
    MRAvgReview.run()
