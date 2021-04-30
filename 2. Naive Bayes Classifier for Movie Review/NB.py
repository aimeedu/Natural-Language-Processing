import os
import math
from pre_process import build_path
import json

def N_doc(dataset, labels):
    ndoc = 0
    for l in labels:
        class_path = build_path(dataset, l)
        temp = len(os.listdir(class_path))
        ndoc += temp
    return ndoc


def prior_prob(dataset, label, ndoc):
    class_path = build_path(dataset, label)
    nc = len(os.listdir(class_path))
    log_c = math.log2(nc/ndoc)
    return log_c

 
log_map = {}    
# vocab = set(line.strip() for line in open('imdb.vocab'))


def train_naive_bayes(labels, vocab, vector_map):
    V = len(vocab) 
    prior_map = {}   
    # count number of docs for all class
    ndoc = N_doc('train', labels)
    print(f"Number of training docs : {ndoc}")
    for c in labels:
        # log prior probabilities
        logprior = prior_prob('train', c, ndoc)
        prior_map[c] = logprior
        # build bag of words
        bag = {}
        total_token = 0
        for f, doc in vector_map["train_" + c].items():
            for k, v in doc.items():
                if k in vocab:
                    total_token += v
                    if k in bag:
                        bag[k] = bag.get(k)+v
                    else:
                        bag[k] = v 
        print(f"Total tokens(repeat) in class {c}:  {total_token}")

        # calculate log likelihood of each word for each class
        conditional_map = {}
        for w in vocab:
            freq = bag.get(w,0)
            # print(f"{freq}, {total_token}")
            log_w_given_c = math.log2((freq+1)/(total_token+V))
            conditional_map[w] = log_w_given_c
        log_map[c] = conditional_map
        # print (len(conditional_map))

    log_map["prior"] = prior_map
    j_string = json.dumps(log_map, indent=4)
    with open('movie_review_BOW.json', 'w') as f:
        f.write(j_string)   
    
    return log_map


def test_one_doc(labels, vocab, log_map, doc, y):
    probs = {}
    for c in labels:    
        # when turn into log probability, we will sum up insted of multipul.
        sum = 0
        # add the log prior probabilities
        sum += log_map["prior"][c]
        # add the conditional prob
        for k, v in doc.items():
            if k in vocab:
                while v>0:
                    sum += log_map[c][k]
                    v -= 1
        probs[c] = sum
    max_val = max(probs.values())  # maximum value
    y_pred = [k for k, v in probs.items() if v == max_val][0]
    return y_pred, probs

def test_naive_bayes(labels, vocab, log_map, vector_map):
    # test for all test docs 
    output = []

    # count total test data
    total_test_doc = 0
    for l in labels:
        total_test_doc += len(vector_map["test_"+l])

    print(f"Number of testing docs : {total_test_doc}")
    correct = 0
    for y in labels:
        list_of_doc = vector_map["test_"+y]
        for f, doc in list_of_doc.items():
            y_pred, probs = test_one_doc(labels, vocab, log_map, doc, y) 
            result = f"given: {y}, predict: {y_pred}, probabilities: {probs}.\n"  
            output.append(result)
            if y == y_pred:
                correct += 1
            else:
                output.append(f)  # get the file name with wrong prediction
                output.append('\n')
    accuracy = correct / total_test_doc * 100
    output.append(f"Overall testing accuracy is {accuracy}%.")
    print(f"*Overall testing accuracy is {accuracy}%.")
    with open ("output.txt", 'w') as f:
        for i in output:
            f.write(i)

def NB(labels, vocab, vector_map):
    train_naive_bayes(labels, vocab, vector_map)
    test_naive_bayes(labels, vocab, log_map, vector_map)

if __name__=="__main__":
    pass