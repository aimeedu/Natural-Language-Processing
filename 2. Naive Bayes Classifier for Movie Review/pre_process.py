import os
import re
import math
import json

# vocab = set(line.strip() for line in open('imdb.vocab'))
vector_map = {}

def build_path(dataset, label):
    # get path automatically
    cwd = os.getcwd()
    path = f"{cwd}/{dataset}/{label}"
    return path

def build_vector(dataset, label, tokens, vocab):
    # build each feature vactor
    vector = {}
    for word in tokens:
        # if dataset == 'train':
        if word in vocab:
            vector[word] = vector.get(word, 0)+1
    return vector

def pre_process_file(dataset, label, vocab):
    vector_label = dataset + "_" +  label
    print(f"{vector_label} done!")
    vectors = {}

    dir_path = build_path(dataset, label)
    file_list = os.listdir(dir_path)


    for file in file_list:
        # print(file)
        file_path = os.path.join(dir_path, file)
        with open(file_path, 'r') as rf:
            # each file contains 1 line, remove all punctuations and only keep the word.
            tokens = re.findall(r"[\w']+", rf.readline())
            # lowercase all token 
            tokens = [token.lower() for token in tokens]
            v = build_vector(dataset, label, tokens, vocab)
            # feature vector returned here, add to the vectors list.
            # vectors.append(v)
            vectors[file] = v
    # add vector to vector_map
    vector_map[vector_label] = vectors
    return 

def pre_process(dataset, labels, vocab):
    print("Vectorizing each directory ...")
    for d in dataset:
        for c in labels:
            pre_process_file(d, c, vocab)
    return vector_map

if __name__=="__main__":
    # pre_process()
    pass
