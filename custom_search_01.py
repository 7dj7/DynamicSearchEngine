from nltk import word_tokenize, pos_tag, ne_chunk 
from nltk import Tree
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import Tree
import pandas as pd
from math import *
import copy
from nltk.corpus import wordnet
# import random as ran
import os

# def shuffle_test_data(filename):
#     curpath = os.path.abspath(os.curdir)
#     filenamepath = os.path.join(curpath,filename)
#     f = open(filenamepath,'r')
#     data = f.readlines()
#     ln = len(data)
#     sdata = ran.sample(data, ln)
#     f.close()
#     newfilename = filename.replace(".txt","-updated.txt") 
#     newfilenamepath = os.path.join(curpath, newfilename)
#     f2 = open(newfilenamepath,'w+')
#     f2.writelines(sdata)
#     f2.close()
# shuffle_test_data('test-case2.txt')

wordnet.synsets('balcony').append('deck')
wordnet.synsets('ground').append(wordnet.synset('deck.n.01'))
print (wordnet.synsets('balcony'))
print (wordnet.synsets('ground'))
import inflect
#this inflect is to extract singular noun 
p = inflect.engine()
#lemmatizer is used to extract the base word from different uses of the word
lemmatizer = WordNetLemmatizer() 

#the stopwords essentually eliminates non signifiant words like I, he, she, am, is, can, should, must, may etc. 
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
        base = lemmatizer.lemmatize(chunk[0])
        #base = chunk[0]
        print('Base word: ' + base)
        print("Used Word:" + str(chunk[0]) + " POS:" + str(chunk[1]))
        if p.singular_noun(base):
            base = p.singular_noun(base)
        base = base.lower()
        if str(chunk[1]) == 'NN' or str(chunk[1]) == 'NNP':
            pos_val[base] = 10.0
        elif str(chunk[1]) == 'JJ' or str(chunk[1]) == 'ADJ' :
            pos_val[base] = 1.0
        elif str(chunk[1]) == 'VB' or str(chunk[1]) == 'VBG' or str(chunk[1]) == 'VBD':
            pos_val[base] = 0.1
        # else:
        #     pos_val[base] = 0.0
    return pos_val
def get_pos_dic_words(document, word=None, chunk_func = ne_chunk):
    chunkedWords = chunk_func(pos_tag(word_tokenize(document)))
    pos_val = {}
    for chunk in chunkedWords:
        if type(chunk) == Tree:
            chunk = chunk.leaves()[0]
        base = lemmatizer.lemmatize(str(chunk[0]).lower())
        #base = chunk[0]
        print('Base word: ' + base)
        print("Used Word:" + str(chunk[0]) + " POS:" + str(chunk[1]))
        if p.singular_noun(base):
            base = p.singular_noun(base)
        if word is None or word == base:
            if str(chunk[1]) == 'NN' or str(chunk[1]) == 'NNP' or str(chunk[1]) == 'NNS':
                pos_val[base] = "N"
            elif str(chunk[1]) == 'JJ' or str(chunk[1]) == 'ADJ' :
                pos_val[base] = "A"
            elif str(chunk[1]) == 'VB' or str(chunk[1]) == 'VBG' or str(chunk[1]) == 'VBD' or str(chunk[1]) == 'VBN':
                pos_val[base] = "V"
    return pos_val
def pos_match_score(valuedoc, valueword, k):
    if valuedoc == valueword:
        return 0.9+k
    elif valuedoc == "N":
        return 0.8+k
    elif valuedoc == "A":
        return 0.7+k
    elif valuedoc == "V":
        return 0.6+k
    else:
        return 0
def word_doc_match_score(keyword, valueword, doc_pos):    
    sim = 0 
    for keydoc,valuedoc in  doc_pos.items():
        if valueword == "N":
            k = 3
        elif valueword == "A":
            k = 2
        else:
            k = 1
        synsdoc = wordnet.synsets(keydoc)
        synsword = wordnet.synsets(keyword) 
        sim = 0
        for doc in synsdoc:
            for word in synsword:
                tempsim = wordnet.wup_similarity(doc, word)
                sim = tempsim if (tempsim is not None and tempsim > sim) else sim
        for syns in synsdoc:
            for l in syns.lemmas(): 
                syn = l.name()
                syn.replace('_', ' ')
                if syn == keyword:
                    return [syn, pos_match_score(valuedoc, valueword, k), sim]
       
            for l in syns.hypernyms(): 
                for syn in list(l.lemma_names('eng')):
                    syn.replace('_', ' ')
                    if syn == keyword:
                        return [syn, pos_match_score(valuedoc, valueword, k), sim]

            for l in syns.hyponyms(): 
                for syn in list(l.lemma_names('eng')):
                    syn.replace('_', ' ')
                    if syn == keyword:
                        return [syn, pos_match_score(valuedoc, valueword, k), sim]

        for syns2 in synsword:
            for l2 in syns2.lemmas():  
                syn2 = l2.name()
                syn2.replace('_', ' ')
                if syn2 == keydoc:
                    return [syn2, pos_match_score(valuedoc, valueword, k), sim]
                
            for l2 in syns2.hypernyms(): 
                for syn2 in list(l2.lemma_names('eng')):
                    syn2.replace('_', ' ')
                    if syn2 == keydoc:
                        return [syn2, pos_match_score(valuedoc, valueword, k), sim]

            for l2 in syns2.hyponyms(): 
                for syn2 in list(l2.lemma_names('eng')):
                    syn2.replace('_', ' ')
                    if syn2 == keydoc:
                        return [syn2, pos_match_score(valuedoc, valueword, k), sim]
    return [None, 0, sim]
# Class for sorting the list and displaying the doc in order
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
    textToSearch = str(' ').join(words)
    keyword_pos = get_pos_dic_words(textToSearch)
    dc = Doc()
    for i,document in enumerate(documents):
        #initial list and order
        print(document)
        words2 = document.split(' ')
        words2 = remove_stop_words(words2)
        document2 = str(' ').join(words2)
        doc_pos = get_pos_dic_words(document2)
        dc = Doc()
        dc.m_nDocID = i + 1
        dc.m_sDocText = document
        dc.m_Dntfreq = {}
        
        for keydoc,valuedoc in  keyword_pos.items():
            [word, score, sim] = word_doc_match_score(keydoc, valuedoc, doc_pos)
            if word is not None:            
            #Get the frequency of the word/term in the document and also see the value /weightage of POS
                dc.m_Dntfreq[word] = score + sim
                dc.m_fntfreq += (score + sim)
            else:
                dc.m_Dntfreq[keydoc] = score

        docs.append(dc)
    #sort as per the term frequency
     #filter if the term freq grearer than 0
    docs = list(filter(lambda Doc:Doc.m_fntfreq>0, docs))
    docs = sorted(docs, key=lambda Doc:Doc.m_fntfreq , reverse=True)
   
    textDocs = []
    for doc in docs:
        #initial list and order
        print(f'Doc ID:{doc.m_nDocID} Text: {doc.m_sDocText} Found Words: {doc.m_Dntfreq.items()}')
        textDocs.append(doc.m_sDocText)
    for doc in docs:
        print(doc.m_sDocText + 'freq:' + str(doc.m_fntfreq))

    curpath = os.path.abspath(os.curdir)
    filenamepath = os.path.join(curpath,"result.txt")
    f2 = open(filenamepath,'w+')
    f2.writelines(textDocs)
    f2.close()
    return textDocs

search('.//test-case2-updated.txt', 'I was sitting on the deck of a fine ship')
