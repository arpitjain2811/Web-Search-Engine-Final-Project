from mrjob.job import MRJob
from nltk.stem import PorterStemmer
import json
import re
import string

stopwords = ["els","tell","expect","thought","noth","usual","anyth","let","wasn","enough","put","told","d","actual","though","took","found","everyth","ll","us","mani","area","someth","feel","came","anoth","said","re","seem","ever","still","everi","made","sinc","around","sure","two","think","lot","see","ask","find","right","locat","didn","give","peopl","way","use","first","went","say","could","thing","much","take","got","never","day","m","tri","nice","come","ve","alway","know","want","well","work","need","also","make","look","even","realli","servic","back","would","good","place","great","one","like","time","go","get","i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"]

PUNC = re.compile('[%s]' % re.escape(string.punctuation))
WORD = re.compile(r"[\w']+")
STOP = re.compile(r'\d+|[^\x00-\x7F]+|\b(' + r'|'.join(stopwords) + r')\b\s*')
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
