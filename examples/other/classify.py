"""
Assignment 3. Implement a Multinomial Naive Bayes classifier for spam filtering.

You'll only have to implement 3 methods below:

train: compute the word probabilities and class priors given a list of documents labeled as spam or ham.
classify: compute the predicted class label for a list of documents
evaluate: compute the accuracy of the predicted class labels.

"""

from collections import defaultdict
import glob
import math
import os



class Document(object):
    """ A Document. Do not modify.
    The instance variables are:

    filename....The path of the file for this document.
    label.......The true class label ('spam' or 'ham'), determined by whether the filename contains the string 'spmsg'
    tokens......A list of token strings.
    """

    def __init__(self, filename=None, label=None, tokens=None):
        """ Initialize a document either from a file, in which case the label
        comes from the file name, or from specified label and tokens, but not
        both.
        """
        if label: # specify from label/tokens, for testing.
            self.label = label
            self.tokens = tokens
        else: # specify from file.
            self.filename = filename
            self.label = 'spam' if 'spmsg' in filename else 'ham'
            self.tokenize()

    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):
    def __init__(self):
        #globals
        
        self.vocab = set() #complete vocab
        #self.vocab_spam = set() #don't need?
        #self.vocab_ham = set() #don't need
        
        self.priorSpam = 0
        self.priorHam = 0
        
        self.cond_prob_ham = {}
        self.cond_prob_spam = {}
    
    
    def get_word_probability(self, label, term):
        """
        Return Pr(term|label). This is only valid after .train has been called.

        Params:
          label: class label.
          term: the term
        Returns:
          A float representing the probability of this term for the specified class.

        >>> docs = [Document(label='spam', tokens=['a', 'b']), Document(label='spam', tokens=['b', 'c']), Document(label='ham', tokens=['c', 'd'])]
        >>> nb = NaiveBayes()
        >>> nb.train(docs)
        >>> nb.get_word_probability('spam', 'a')
        0.25
        >>> nb.get_word_probability('spam', 'b')
        0.375
        """
        ###DONE
        if 'spam' in label:
            return self.cond_prob_spam[term]
        elif 'ham' in label:
            return self.cond_prob_ham[term]
        else:
            print("Just run the doctest Dev")
            
        pass

    def get_top_words(self, label, n):
        """ Return the top n words for the specified class, using the odds ratio.
        The score for term t in class c is: p(t|c) / p(t|c'), where c'!=c.

        Params:
          labels...Class label.
          n........Number of values to return.
        Returns:
          A list of (float, string) tuples, where each float is the odds ratio
          defined above, and the string is the corresponding term.  This list
          should be sorted in descending order of odds ratio.

        >>> docs = [Document(label='spam', tokens=['a', 'b']), Document(label='spam', tokens=['b', 'c']), Document(label='ham', tokens=['c', 'd'])]
        >>> nb = NaiveBayes()
        >>> nb.train(docs)
        >>> nb.get_top_words('spam', 2)
        [(2.25, 'b'), (1.5, 'a')]
        """
        ###DONE
        score_list = []
        if('spam' in label):
            for term in self.vocab:
                score = self.cond_prob_spam[term] / self.cond_prob_ham[term]
                score_list.append((score,term))       
        else:
            for term in self.vocab:
                score = self.cond_prob_ham[term] / self.cond_prob_spam[term]
                score_list.append((score,term))
        score_list = sorted(score_list, key=lambda x:x[0],reverse=True)[:n]
        return score_list         
        pass

    def train(self, documents):
        """
        Given a list of labeled Document objects, compute the class priors and
        word conditional probabilities, following Figure 13.2 of your
        book. Store these as instance variables, to be used by the classify
        method subsequently.
        Params:
          documents...A list of training Documents.
        Returns:
          Nothing.
        """
        ###DONE
        
        #entire vocab in document set D
        vocab_spam = set()
        vocab_ham = set()
        
        #Calcuates prior probabilities
        priorSPAM = 0 #how many docs are spam
        priorHAM = 0 #how many docs are ham
        
        #Cacluates Tct
        term_freq_spam = {} #{term:occur, term:occur}
        term_freq_ham = {}
        
        #Tct'
        Tct_Spam = 0 #Tct' = sum of (every term occurence in class c + 1)
        Tct_Ham = 0
        
        for doc in documents: 
            if(doc.label == 'spam'):
                priorSPAM += 1
                for token in doc.tokens:
                    Tct_Spam += 1
                    if token in term_freq_spam.keys():
                        term_freq_spam[token] = term_freq_spam[token] + 1
                    else:
                        term_freq_spam[token] = 1
                        vocab_spam.add(token) 
            else:
                priorHAM += 1
                for token in doc.tokens:
                    Tct_Ham += 1
                    if token in term_freq_ham.keys():
                        term_freq_ham[token] = term_freq_ham[token] + 1
                    else:
                        term_freq_ham[token] = 1
                        vocab_ham.add(token)
        
        
        #endfor
        # | is for set join
        self.vocab = vocab_spam | vocab_ham #gets rid of duplicate words (those in both 'ham' and 'spam')        
        
        #Tct Primes
        #tct' = term freq of all terms in class c + 1*(total terms)
        Tct_Spam = Tct_Spam + len(self.vocab) 
        Tct_Ham = Tct_Ham + len(self.vocab) 
        
        self.priorSPAM = priorSPAM / len(documents)
        self.priorHAM = priorHAM / len(documents)
        
        """ #this doesn't work for all terms (prob of term in 
        for term in vocab_ham:
            self.cond_prob_ham[term] = (term_freq_ham[term] + 1) / Tct_Ham
        for term in vocab_spam:
            self.cond_prob_spam[term] = (term_freq_spam[term] + 1) / Tct_Spam 
        """
        
        for term in self.vocab:
            if term in term_freq_ham.keys():
                self.cond_prob_ham[term] = (term_freq_ham[term] + 1) / Tct_Ham
            else:
                self.cond_prob_ham[term] = 1 / Tct_Ham
            
            if term in term_freq_spam.keys():
                self.cond_prob_spam[term] = (term_freq_spam[term] + 1) / Tct_Spam
            else:
                self.cond_prob_spam[term] = 1 / Tct_Spam
            
        
        pass

    def classify(self, documents):
        """ Return a list of strings, either 'spam' or 'ham', for each document.
        Params:
          documents....A list of Document objects to be classified.
        Returns:
          A list of label strings corresponding to the predictions for each document.
        """
        ###TODO
        predictions = []
        for doc in documents:
            score_spam = math.log(self.priorSPAM)
            score_ham = math.log(self.priorHAM)
            for term in doc.tokens:
                if term in self.cond_prob_spam.keys():
                    score_spam += math.log(self.cond_prob_spam[term])
                if term in self.cond_prob_ham.keys():
                    score_ham += math.log(self.cond_prob_ham[term])
            if(score_ham >= score_spam): #defaults to ham if score = even                    
                predictions.append('ham')
            else:
                predictions.append('spam')
                
        return predictions        
        pass

def evaluate(predictions, documents):
    """ Evaluate the accuracy of a set of predictions.
    Return a tuple of three values (X, Y, Z) where
    X = percent of documents classified correctly
    Y = number of ham documents incorrectly classified as spam
    Z = number of spam documents incorrectly classified as ham

    Params:
      predictions....list of document labels predicted by a classifier.
      documents......list of Document objects, with known labels.
    Returns:
      Tuple of three floats, defined above.
    """
    ###TODO
    x = 0.0
    y = 0 #true ham, classified spam
    z = 0 #true spam, classified ham
    
    for i in range(0,len(predictions)):
        if(documents[i].label == 'spam' and predictions[i] == 'ham'):
            z += 1
        if(documents[i].label == 'ham' and predictions[i] == 'spam'):
            y += 1        
    
    x = (len(documents) - (y+z)) / len(documents) 
    return (x,y,z)
    pass

def main():
    """ Do not modify. """
    if not os.path.exists('train'):  # download data
       from urllib.request import urlretrieve
       import tarfile
       urlretrieve('http://cs.iit.edu/~culotta/cs429/lingspam.tgz', 'lingspam.tgz')
       tar = tarfile.open('lingspam.tgz')
       tar.extractall()
       tar.close()
    
    train_docs = [Document(filename=f) for f in glob.glob("train/*.txt")]
    print('read', len(train_docs), 'training documents.')
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(filename=f) for f in glob.glob("test/*.txt")]
    print('read', len(test_docs), 'testing documents.')
    predictions = nb.classify(test_docs)
    results = evaluate(predictions, test_docs)
    print('accuracy=%.3f, %d false spam, %d missed spam' % (results[0], results[1], results[2]))
    print('top ham terms: %s' % ' '.join('%.2f/%s' % (v,t) for v, t in nb.get_top_words('ham', 10)))
    print('top spam terms: %s' % ' '.join('%.2f/%s' % (v,t) for v, t in nb.get_top_words('spam', 10)))
   
if __name__ == '__main__':
    main()
