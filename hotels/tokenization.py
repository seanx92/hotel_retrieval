import json
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import RegexpStemmer
from nltk.corpus import stopwords
import re

def tokenize(doc): 
    """This function used to tokenize each document. 

    The entrance of this list of function. Take a string as input.
    """
    result = nltk.word_tokenize(doc)
    result = clean(result)
    for i in range(len(result)):
        result[i] = normalize(result[i])
        result[i] = stemming(result[i]).encode('utf-8')
    return result

def normalize(word):
    """Normalize a word

    """
    result = word
    if '.' in result: #normalize acronym to form without period
        re.sub('.', '', result)
    return word.lower() #normalize word to lower case

def stemming(word):
    """stemming a word by using snowball stemmer
 
    """
    SB_stemmer = SnowballStemmer("english")
    return SB_stemmer.stem(word)

def clean(words):
    """Used to exclue stop words and seperate words that not proper formatted in original doc

    """
    result = []
    result_candidates = []
    for i in range(len(words)):    #handle the situation there is no space before or after a period
        words[i] = words[i].strip(' (),.;:\'|"\\/<>')
        if '.' in words[i] and re.search('[a-z](?![A-Z])(.(?![A-Z]))*' , words[i]):
            result_candidates.extend(words[i].split('.'))
        else:
            result_candidates.append(words[i])
    for candidate in result_candidates:
        if re.match('^[A-z0-9]+$', candidate) and candidate not in stopwords.words('english'):
            result.append(candidate)
    return result
