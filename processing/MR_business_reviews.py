from mrjob.job import MRJob
import json

class MRBusinessReview(MRJob):

    def mapper(self, _, line):
        obj = json.loads(line)
        yield obj['business_id'], obj['text'].replace('\n', ' ')

    def reducer(self, key, values):
        yield key, " ".join(values)

if __name__ == '__main__':
    MRBusinessReview.run()
