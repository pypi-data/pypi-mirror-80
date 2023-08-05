#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from re import sub
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk.tokenize import RegexpTokenizer, sent_tokenize, word_tokenize
from nltk import download
from tqdm import tqdm
download("punkt")

def text_normalize(text, method = 'lemmas'):
    """
    
    Parameters
    ----------
    text: str
        List or pandas column of texts as string
    method: str, {'lemmas','stems'}, default 'lemmas'
        Normalization method used on text.
    
    Returns
    -------
    normalized_text: list
        List of lists with lemmas or stems as strings
    
    Examples
    --------
    normalize text with lemmas
    
    >>> dickens = ["It was the best of times.", "it was the worst of times!"]
    >>> normalized_text = px.text_normalize(dickens, method = 'lemmas')
    >>> normalized_text
    [['it', 'be', 'the', 'best', 'of', 'time'],
    ['it', 'be', 'the', 'worst', 'of', 'time']]
    
    """
    if method == 'lemmas':
        normalizer = WordNetLemmatizer()
    if method == 'stems':
        normalizer = PorterStemmer()
    temp = []
    for i in tqdm(range(len(text))):
        words = word_tokenize(text[i])
        words=[word.lower() for word in words if word.isalpha()]
        if method == 'lemmas':
            temp.append([normalizer.lemmatize(w, pos='v') for w in words])
        if method == 'stems':
            temp.append([normalizer.stem(w) for w in words])
    return temp


def clean_text(text,replace = None, replace_with = '', lower_case = False):
    """
    
    Parameters
    ----------
    text: str
        List or pandas column of texts as string
    replace: str
        Regular expression to be replaced
    replace_with: str
        Regular expression to be used as replacement for expression in `replace`
    lower_case: bool, default False
        Convert text to lower case before cleaning
        
    Returns
    -------
    cleaned_list: list
        list of strings with `replace_with` regular expression in place of `replace` regulare expression
        
    Examples
    --------
    >>> ATCQ = "Can I kick it? To all the people who can Quest like A Tribe does"
    >>> response = px.clean_text(ATCQ, replace= 'To all the people who can Quest like A Tribe does', replace_with= 'Yes you can!', lower_case=False)
    >>> response
    ['Can I kick it? Yes you can!']
    
    
    """
    clean_temp = []
    for t in tqdm(text):
        temp = []
        if lower_case == True:
            t = t.lower()  
        else:
            t = t
        t = sub(replace,replace_with,str(t))
        temp.append(t)
        clean_temp.append(temp)
    return [i for sublist in clean_temp for i in sublist]

def concat_normtext(text):
    """
    concatenate list of normalized text into one string
    
    Parameters
    ----------
    text: str
        List or pandas column of texts as string
    
    Returns
    -------
    cleaned_list: list
    
    Examples
    --------
    >>>normalized_text = [['it', 'be', 'the', 'best', 'of', 'time'], ['it', 'be', 'the', 'worst', 'of', 'time']]
    >>>result = px.concat_normtext(normalized_text)
    >>>result
    [' it be the best of time', ' it be the worst of time']
    
    """
    temp_text = []
    for t in text:
        string = ""
        if t == []:
            temp = t
            for i in t:
                string = string + " " + i            
        else:
            for i in t:
                temp = []
                string = string + " " + i
        temp.append(string)
        temp_text.append(temp)
    return [i for sublist in temp_text for i in sublist]

