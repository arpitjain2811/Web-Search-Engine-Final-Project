from mrjob.job import MRJob
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import json
import re
import string


PUNC = re.compile('[%s]' % re.escape(string.punctuation))
WORD = re.compile(r"[\w']+")
STOP = re.compile(r'\d+|[^\x00-\x7F]+|\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
PS = PorterStemmer()

class MRBusinessSim1(MRJob):

    def mapper(self, _, line):
        obj = json.loads(line)

        words = WORD.findall(STOP.sub('', PUNC.sub(' ', obj['text'].lower())))

        stemmed = [PS.stem(word) for word in words]

        word_counts = {}
        for w in stemmed:
            if w not in word_counts.keys():
                word_counts[w] = 1
            else:
                word_counts[w] += 1

        yield obj['business_id'], word_counts.items()
        

    def reducer(self, key, values):
        word_counts = {}
        for val in values:
            for pair in val:
                if pair[0] not in word_counts.keys():
                    word_counts[pair[0]] = pair[1]
                else:
                    word_counts[pair[0]] += pair[1]

        for k, v in word_counts.items():
            yield k, (key, v)

if __name__ == '__main__':
    MRBusinessSim1.run()
