# implement the Naive Bayes classifier for movie review classification.
import math
import os
import sys
from NB import NB
from pre_process import pre_process

def main():
    dataset = ["train", "test"]
      
    # 1. Sentiment Analysis ----------------------------------------------------
    labels = ['neg', 'pos'] 
    vocab = set(line.strip() for line in open('imdb.vocab'))
        
    # # 2. Text Classification -------------------------------------------------
    # labels = ['comedy', 'action']
    # vocab = {"fun", "couple", "love", "fly", "fast", "furious", "shoot"}

    # tonkenizer all the data, and output vector format.
    vector_map = pre_process(dataset, labels, vocab)
    
    # call Naive Bayes classifier with pre-processed data.
    NB(labels, vocab, vector_map)

if __name__=="__main__":
    main()