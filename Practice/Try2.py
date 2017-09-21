import nltk, re, pprint
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

stop = stopwords.words('english')

def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	filtered_words = [w for w in tokens if not w in stopwords.words('english')]
	return " ".join(filtered_words)

def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences[0]

file1= open("FirstPage.txt","r")
string = file1.read()
print(string)
string = preprocess(string)
string = ie_preprocess(string)
print(string)

grammer = r"""
        NP: {<NN><JJ.*>*<NN.*>*<VB.*>+}
           """
cp = nltk.RegexpParser(grammer)
result = cp.parse(string)
print(result)
result.draw()
