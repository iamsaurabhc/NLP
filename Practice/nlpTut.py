import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize, sent_tokenize
import nltk.data
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem import PorterStemmer

def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	filtered_words = [w for w in tokens if not w in stopwords.words('english')]
	return " ".join(tokens)

file1= open("FirstPage.txt","r")
text = file1.read()

text = preprocess(text)
words = word_tokenize(text)
tagged = nltk.pos_tag(words)
chunkGram = r"""
Parties: {<NN>?<JJ><NN.?>+<VB.?>}
"""

chunkParser = nltk.RegexpParser(chunkGram)
result = chunkParser.parse(tagged)
print(result)
i=-1
parties = ["",""]
for res in result.subtrees():
	if res.label() == 'Parties':
		i=i+1
		if(i==2):
			break
		for l in res.leaves():
			parties[i] += str(l[0]+" ")
    #print(res)
    #print(res.leaves()[0])
print(parties[1])
