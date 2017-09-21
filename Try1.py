# information-extraction.py

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
stop = stopwords.words('english')

file1= open("ordjud.txt","r")
string = file1.read()
'''
string = """
Hey,
This week has been crazy, but I met Mark Peterson this week. Attached is my report on IBM. Can you give it a quick read and provide some feedback.
Also, make sure you reach out to Claire (claire@xyz.com).
You're the best.
Cheers,
George W.
James Mule
212-555-1234
"""
'''
def extract_court_name(string):
    list_of_words = string.split()
    count_name = list_of_words[list_of_words.index("JUDICATURE")+2]
    return count_name
def extract_plaintiff_names(string):
    list_of_words = string.split()
    plaintiff_name = list_of_words[list_of_words.index("...Plaintiff")]

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    tokenizer = RegexpTokenizer(r'\w+')
    sentences = tokenizer.tokenize(document)
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    print(sentences)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names

if __name__ == '__main__':
    numbers = extract_phone_numbers(string)
    emails = extract_email_addresses(string)
    names = extract_names(string)
    courtName = extract_court_name(string)
    print(names)
