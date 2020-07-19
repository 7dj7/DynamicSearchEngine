from nltk import word_tokenize, pos_tag, ne_chunk 
from nltk.corpus import stopwords
from nltk import RegexpParser
from nltk import Tree
import pandas as pd
from math import *
import copy
import inflect
p = inflect.engine()
stop_words = set(stopwords.words('english'))
# Load data
def load_data(path):
    dataframe = pd.read_csv(path)
    return dataframe
def load_txt_data(path):
    f = open(path,'r')
    data = f.readlines()
    f.close()
    return data

# Get the pos of the searched strings
def get_pos_val(text, chunk_func = ne_chunk):
    chunkedWords = chunk_func(pos_tag(word_tokenize(text)))
    pos_val = {}
    for chunk in chunkedWords:
        print("Word:" + str(chunk[0]) + " POS:" + str(chunk[1]))
        if str(chunk[1]) == 'NN' or str(chunk[1]) == 'NNP':
            pos_val[chunk[0]] = 1
        elif str(chunk[1]) == 'VB' or str(chunk[1]) == 'VBG' or str(chunk[1]) == 'VBD':
            pos_val[chunk[0]] = 0.8
        else:
            pos_val[chunk[0]] = 0.6
    return pos_val

def normalized_term_frequency(word, document):
    if p.singular_noun(word):
        word = p.singular_noun(word)
    word = word.lower()
    document = document.strip('\n')
    storedWords = document.split('\xa0')
    if len(storedWords) == 1:
        storedWords = document.split(' ')
    raw_frequency = 0
    for stword in storedWords:
        if p.singular_noun(stword):
            stword = p.singular_noun(stword)
        stword = stword.lower()
        if stword == word:
            raw_frequency += 1
    #raw_frequency = document.count(word)
    if raw_frequency == 0:
        return 0
    return 1 + log(raw_frequency)

class Doc:
    m_nDocID = 0
    m_Dntfreq = {}
    m_fntfreq = 0
    m_sDocText = ''
    def __init__(self, other = None):
        if other is None:
            self.non_copy_constructor()
        else:
            self.copy_constructor(other)
    def non_copy_constructor(self):
        return
    def copy_constructor(self, other):
        self.m_Dntfreq = copy.deepcopy(other.m_Dntfreq)
        self.m_sDocText = copy.deepcopy(other.m_sDocText)
        self.m_nDocID = other.m_nDocID
        self.m_fntfreq = other.m_fntfreq
     
def remove_stop_words(words):
    new_words = []
    for w in words:
        if w not in stop_words:
            new_words.append(w)
    return new_words
def search(path, textToSearch):
    ###Get the list of documents
    documents = load_txt_data(path)
    docs = []
    #keep a phrase as the original text and also keep separate single keywords
    textToSearch = textToSearch.lower() 
    words = textToSearch.split(' ')
    words = remove_stop_words(words)
    posVals = get_pos_val(textToSearch)
    dc = Doc()
    for i,document in enumerate(documents):
        #initial list and order
        print(document)
        dc = Doc()
        dc.m_nDocID = i + 1
        dc.m_sDocText = document
        dc.m_Dntfreq = {}
        freqPh = normalized_term_frequency(textToSearch, document)
        dc.m_Dntfreq[textToSearch] = freqPh
        dc.m_fntfreq = freqPh
        for word in words:            
        #Get the frequency of the word/term in the document and also see the value /weightage of POS
            freq = normalized_term_frequency(word, document)
            if posVals[word] is not None:
                dc.m_Dntfreq[word] = freq*posVals[word]
            else:
                dc.m_Dntfreq[word] = freq
            dc.m_fntfreq += freq
        docs.append(dc)
    #sort as per the term frequency
    docs = sorted(docs, key=lambda Doc:Doc.m_fntfreq , reverse=True)
    for doc in docs:
        #initial list and order
        print(f'Doc ID:{doc.m_nDocID} Text: {doc.m_sDocText} Found Words: {doc.m_Dntfreq.items()}')
 
search('test_cases.csv', 'ship')
