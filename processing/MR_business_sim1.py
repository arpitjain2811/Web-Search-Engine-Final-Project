from mrjob.job import MRJob
from nltk.tokenize import word_tokenize
import json
import re

WORD_RE = re.compile(r"[\w']+")

class MRBusinessSim1(MRJob):

    def mapper(self, _, line):
        obj = json.loads(line)
        words = {}
#        tokenized = word_tokenize(line)
        for word in WORD_RE.findall(obj['text']):
            if word.lower() in words.keys():
                words[word.lower()] += 1
            else:
                words[word.lower()] = 1
        for k, v in words.items():
            yield (obj['business_id'], k), v

    def reducer(self, key, values):
        yield key[1], (key[0], sum(values))
        

if __name__ == '__main__':
    MRBusinessSim1.run()
