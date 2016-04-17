#!python
from collections import defaultdict
import glob
import math
import os

class Document(object):
    """ A Document. Do not modify.
    The instance variables are:
    id: postID
    popular:TRUE/FALSE
    LIKES: Likes
    Text: text
    
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
            self.postID = -1
            self.likes = -1
        else: # specify from file.
            self.filename = filename
            parsedNames = filename.split("#")
            if 'pop' in parsedNames[0]:
                self.label = 'pop'
            else:
                self.label = 'sod'
            self.postID = parsedNames[1]
            self.likes = parsedNames[2]
            self.tokenize()



    def tokenize(self):
        self.tokens = ' '.join(open(self.filename).readlines()).split()


class NaiveBayes(object):
    def __init__(self):
        #globals
        
        self.vocab = set() #complete vocab 
                
        self.priorSod = 0
        self.priorPop = 0
        
        self.cond_prob_pop = {}
        self.cond_prob_sod = {}
    
    
    def get_word_probability(self, label, term):
        """
        Return Pr(term|label). This is only valid after .train has been called.

        Params:
          label: class label.
          term: the term
        Returns:
          A float representing the probability of this term for the specified class.
        """

        if 'sod' in label:
            return self.cond_prob_sod[term]
        elif 'pop' in label:
            return self.cond_prob_pop[term]
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
        """
        score_list = []
        if('sod' in label):
            for term in self.vocab:
                score = self.cond_prob_sod[term] / self.cond_prob_pop[term]
                score_list.append((score,term))       
        else:
            for term in self.vocab:
                score = self.cond_prob_pop[term] / self.cond_prob_sod[term]
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
        vocab_sod = set()
        vocab_pop = set()
        
        #Calcuates prior probabilities
        priorSOD = 0 #how many docs are spam
        priorPOP = 0 #how many docs are ham
        
        #Cacluates Tct
        term_freq_sod = {} #{term:occur, term:occur}
        term_freq_pop = {}
        
        #Tct'
        Tct_sod = 0 #Tct' = sum of (every term occurence in class c + 1)
        Tct_pop = 0
        
        for doc in documents: 
            if 'sod' in doc.label:
                priorSOD += 1
                for token in doc.tokens:
                    Tct_sod += 1
                    if token in term_freq_sod.keys():
                        term_freq_sod[token] = term_freq_sod[token] + 1
                    else:
                        term_freq_sod[token] = 1
                        vocab_sod.add(token) 
            else:
                priorPOP += 1
                for token in doc.tokens:
                    Tct_pop += 1
                    if token in term_freq_pop.keys():
                        term_freq_pop[token] = term_freq_pop[token] + 1
                    else:
                        term_freq_pop[token] = 1
                        vocab_pop.add(token)
        
        
        #endfor
        # | is for set join
        self.vocab = vocab_sod | vocab_pop #gets rid of duplicate words (those in both 'ham' and 'spam')        
        
        #Tct Primes
        #tct' = term freq of all terms in class c + 1*(total terms)
        Tct_sod = Tct_sod + len(self.vocab) 
        Tct_pop = Tct_pop + len(self.vocab) 
       
        
        print("PriorSod: " + str(priorSOD))
        print("PriorPop: " + str(priorPOP))
        print("LEN Docum: " + str(len(documents)))
        
        self.priorSOD = priorSOD / len(documents)
        self.priorPOP = priorPOP / len(documents)
        
        for term in self.vocab:
            if term in term_freq_pop.keys():
                self.cond_prob_pop[term] = (term_freq_pop[term] + 1) / Tct_pop
            else:
                self.cond_prob_pop[term] = 1 / Tct_pop
            
            if term in term_freq_sod.keys():
                self.cond_prob_sod[term] = (term_freq_sod[term] + 1) / Tct_sod
            else:
                self.cond_prob_sod[term] = 1 / Tct_sod
            
        
        pass

    def classify(self, documents):
        """ Return a list of strings, either 'spam' or 'ham', for each document.
        Params:
          documents....A list of Document objects to be classified.
        Returns:
          A list of label strings corresponding to the predictions for each document.
        """
        predictions = []
        for doc in documents:

            score_sod = math.log(self.priorSOD)
            score_pop = math.log(self.priorPOP)
            for term in doc.tokens:
                if term in self.cond_prob_sod.keys():
                    score_sod += math.log(self.cond_prob_sod[term])
                if term in self.cond_prob_pop.keys():
                    score_pop += math.log(self.cond_prob_pop[term])
            if(score_pop >= score_sod): #defaults to ham if score = even                    
                predictions.append('pop')
            else:
                predictions.append('sod')
                
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
        if(documents[i].label == 'sod' and predictions[i] == 'pop'):
            z += 1
        if(documents[i].label == 'sod' and predictions[i] == 'pop'):
            y += 1        
    
    x = (len(documents) - (y+z)) / len(documents) 
    return (x,y,z)
    pass

def main():
    if not os.path.exists('train'):  # download data
       print("Please run datascraper to create dataset")
    
    train_docs = [Document(filename=f) for f in glob.glob("train/*.txt")]
    print('read', len(train_docs), 'training documents.')
    nb = NaiveBayes()
    nb.train(train_docs)
    test_docs = [Document(filename=f) for f in glob.glob("test/*.txt")]
    print('read', len(test_docs), 'testing documents.')
    predictions = nb.classify(test_docs)
    results = evaluate(predictions, test_docs)
    print('accuracy=%.3f, %d false sod, %d missed sod' % (results[0], results[1], results[2]))
    print('top pop terms: %s' % ' '.join('%.2f/%s' % (v,t) for v, t in nb.get_top_words('pop', 10)))
    print('top sod terms: %s' % ' '.join('%.2f/%s' % (v,t) for v, t in nb.get_top_words('sod', 10)))
   
if __name__ == '__main__':
    main()
