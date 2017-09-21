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

#File preprocessing function
def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'\w+')
	tokens = tokenizer.tokenize(sentence)
	#filtered_words = [w for w in tokens if not w in stopwords.words('english')]
	return " ".join(tokens)

#Information Extraction preprocessing function
def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document) #Sentence tokenizing
    sentences = [nltk.word_tokenize(sent) for sent in sentences] #word tokenizing
    #sentences = [nltk.pos_tag(sent) for sent in sentences] #part of speech tagging
    return sentences[0]

def extract_parties(words):
    parties = []
    for w in words:
        if w == 'plaintiff':
            requiredText = words[words.index(w)-10:words.index(w)+10]
            break
    requiredTextTagged = nltk.pos_tag(requiredText)
    # Chunking with Regular Expressions
    chunkGram = r"""
    Parties1: {<NN>?<JJ><NN.?>+<VB.?>}
    """
    chunkParser = nltk.RegexpParser(chunkGram)
    result = chunkParser.parse(requiredTextTagged)
    i=-1
    for res in result.subtrees():
    	if res.label() == 'Parties1':
    		i=i+1
    		if(i==2):
    			break
    		parties.append(' '.join([l[0] for l in res.leaves()]))
    return parties

def getCounselDetailPara(words):
    applicantCounselGroup = []
    respondentCounselGroup = []

    for w in words:
        if w == 'advocate' or w == 'adv':
            counselPara = words[words.index(w)-5:words.index(w)+40]
    for w in counselPara:
        if w == 'applicant' or w == 'plaintiff':
            applicantCounselGroup = counselPara[0:counselPara.index(w)]
            respondentCounselGroup = counselPara[counselPara.index(w)+1:len(counselPara)]

    return applicantCounselGroup,respondentCounselGroup

def extractApplicantCounselGroup(words):
    applicantCounselGroup = []

    applicantCounsel,_ = getCounselDetailPara(preprocessedText)

    advocatesTagged = nltk.pos_tag(applicantCounsel)

    # Chunking with Regular Expressions
    chunkGram = r"""
    applicantAdvocate1n3: {<NN>{3,3}<NN>*}
    applicantAdvocate2: {<NN><VBD><JJ>}
    applicantAdvocate4: {<JJ><NN><NN>}
    applicantAdvocate5: {<NN><JJ><NN><NNS>}
    """
    chunkParser = nltk.RegexpParser(chunkGram)
    result = chunkParser.parse(advocatesTagged)

    for res in result.subtrees():
    	if (
        res.label() == 'applicantAdvocate1n3' or res.label() == 'applicantAdvocate2' or
        res.label() == 'applicantAdvocate4'   or res.label() == 'applicantAdvocate5'
        ):
            applicantCounselGroup.append(' '.join([l[0] for l in res.leaves()]))

    return applicantCounselGroup

def extractRespondentCounselGroup(preprocessedText):
    respondentCounselGroup = []

    _, respondentCounsel = getCounselDetailPara(preprocessedText)

    advocatesTagged = nltk.pos_tag(respondentCounsel)

    # Chunking with Regular Expressions
    chunkGram = r"""
    respondentAdvocate1: {<NN>{2,2}<VBD>}
    respondentAdvocate2: {<NN><DT>{2,2}<NN>}
    respondentAdvocate3: {<NN>{2,2}<JJ>{2,2}}
    """
    chunkParser = nltk.RegexpParser(chunkGram)
    result = chunkParser.parse(advocatesTagged)

    for res in result.subtrees():
    	if (
        res.label() == 'respondentAdvocate1' or res.label() == 'respondentAdvocate2' or
        res.label() == 'respondentAdvocate3'
        ):
            respondentCounselGroup.append(' '.join([l[0] for l in res.leaves()]))

    return respondentCounselGroup

#Extract Court Name function
def extract_court_name(string):
    list_of_words = string.split()
    count_name = list_of_words[list_of_words.index("JUDICATURE")+2]
    return count_name
