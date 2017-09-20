import pdfquery
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re

import nltk, re, pprint
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tag import pos_tag
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords

from enchant.checker import SpellChecker

stop = stopwords.words('english')

#Convert PDF to TXT function
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

#TXT file preprocessing function
def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	filtered_words = [w for w in tokens if not w in stopwords.words('english')]
	return " ".join(filtered_words)

#Information Extraction preprocessing function
def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document) #Sentence tokenizing
    sentences = [nltk.word_tokenize(sent) for sent in sentences] #word tokenizing
    sentences = [nltk.pos_tag(sent) for sent in sentences] #part of speech tagging
    return sentences[0]

#Extract Court Name function
def extract_court_name(string):
    list_of_words = string.split()
    count_name = list_of_words[list_of_words.index("JUDICATURE")+2]
    return count_name

#Extract Plaintiff Names function
def extract_plaintiff_names(string):
    list_of_words = string.split()
    plaintiff_name = list_of_words[list_of_words.index("...Plaintiff")]
    return plaintiff_name

#Extract Names within the given document function
def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    #print(sentences)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

# First Step: Convert PDF to TEXT for further processing
pdfFile = "ordjud2.pdf"
raw_text = convert_pdf_to_txt(pdfFile)

## Extra Step : Save the text in a .txt file for future processing
fp = open("ordjud2.txt","w")
fp.write(raw_text)
fp.close()

# preprocess the Text extracted
text_preprocessed = preprocess(raw_text)
string = ie_preprocess(text_preprocessed)
#print(string)

# Extract Court names and Names within the document
names = extract_names(raw_text)
courtName = extract_court_name(string)
print(courtName)
print(names)

# Chunking with Regular Expressions
grammer = r"""
        NP: {<NN><JJ.*>*<NN.*>*<VB.*>+}
           """
cp = nltk.RegexpParser(grammer)
result = cp.parse(string)
print(result)
result.draw()
