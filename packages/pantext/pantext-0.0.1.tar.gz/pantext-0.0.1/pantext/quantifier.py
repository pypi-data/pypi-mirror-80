#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from nltk.corpus import stopwords
from nltk import download
from re import sub
from nltk.tokenize import RegexpTokenizer, sent_tokenize, word_tokenize
from tqdm import tqdm

download('stopwords')
download('wordnet')

class Quantifier:
    """
    class for quantifying aspects of text in a list or pandas column
    
    Parameters
    ----------
    text: str
        List or pandas column of texts as string
    
    """
    def __init__(self,text):
        self.text = text
    
        #sentence count 
    def sent_count(self):
        """
        count sentences in each piece of text.
        
        Returns
        -------
        count_list: list
            Returns a list of sentence counts per string in list
        
        Examples
        --------
        >>> text = ["'Anselmo,' the old man said. 'I am called Anselmo and I  come from Barco deAvila. Let me help you with that pack'"]
        >>> Q = px.Quantifier(text)
        >>> Q.sent_count()
        [3]
        """
        count = []
        for i in tqdm(self.text):
            count.append(len(sent_tokenize(i)))
        return count

    #regex counter can count any type of regular expression occurrences in text default words
    def counts(self, regex = "\w+"):
        """
        count regex item in each piece of text.
        
        Parameters
        ----------
        regex: string, default "\w+"
            regular expresion to count in text. Default is counting words
        
        Returns
        -------
        count_list: list
            Returns a list of regex counts per string in list
        
        Examples
        --------
        >>> text = ["'Anselmo,' the old man said. 'I am called Anselmo and I  come from Barco deAvila. Let me help you with that pack'"]
        >>> Q = px.Quantifier(text)
        >>> Q.counts(regex = "\w+")
        [22]
        """        
        tokenizer = RegexpTokenizer(r'{}'.format(regex))
        count = []
        for i in tqdm(self.text):
            count.append(len(tokenizer.tokenize(i)))
        return count

    #counts percentage of words in text that are stopwords
    def stopword_percent(self, stop_words = 'english'):
        """
        generate stopword percentage in each piece of text.
        
        Parameters
        ----------
        stop_words: str, default 'english'
            see nltk.corpus.stopwords for languages
            
        Returns
        -------
        count_list: list
            Returns a list of percentage of stopwords per string in list
        
        Examples
        --------
        >>> text = ["'Anselmo,' the old man said. 'I am called Anselmo and I  come from Barco deAvila. Let me help you with that pack'"]
        >>> Q = px.Quantifier(text)
        >>> Q.stopword_percent(stop_words = 'english')
        [0.36]
        """ 
        stops = set(stopwords.words(stop_words))
        percent = []
        for i in tqdm(self.text):
            text_l = i.lower()
            word_tokens = word_tokenize(text_l)
            stop_w = [word for word in word_tokens if word in stops]
            if len(stop_w) == 0:
                percent.append(0.0)
            else:
                percent.append(round((len(stop_w)/len(word_tokens)), 2))
        return percent

