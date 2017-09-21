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

from enchant.checker import SpellChecker

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
def Information_Extraction_Preprocess(document):
    sentences = sent_tokenize(document)
    sentences = [word_tokenize(sent) for sent in sentences]
    #sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def Spell_Checker(doc):
    checker = SpellChecker("en_IN")
    checker.set_text(doc)
    for error in checker:
        for suggestion in error.suggest():
            if error.word.replace(' ', '') == suggestion.replace(' ', ''):  # make sure the suggestion has exact same characters as error in the same order as error and without considering spaces
                error.replace(suggestion)
                break
    return checker.get_text()



# First Step: Convert PDF to TEXT for further processing
file_name = "ordjud2.pdf"
raw = convert_pdf_to_txt(file_name)
raw_checked = Spell_Checker(raw)

## Extra Step : Save the text in a .txt file
fp = open("ordjud2.txt","w")
fp.write(raw_checked)
fp.close()

# Second Step: Read the .txt file


#text_tokenized = Information_Extraction_Preprocess(raw_checked)

print(raw_checked)
#text_tokenized = word_tokenize(raw_checked)

#text = nltk.Text(text_tokenized)
#print(text)
#match = text.concordance('defendant')
#print(text)
#tagged = pos_tag(text_tokenize)
#print(tagged)


#tokens = word_tokenize(text)
#print(tokens)
#tokens.similar('Applicant')
# Second Step: Tokenize sentences of the extracted text
#
#print(tokens)
#print(nltk.pos_tag(text))
#Information_Extraction_Preprocess(text)


#opinion = TextBlob(text)
#opinion = TextBlob(text, analyzer=NaiveBayesAnalyzer())
#print(opinion.sentiment)

#print(text)
