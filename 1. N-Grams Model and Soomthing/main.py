import math
import sys

# 1st preprocessing: padding with <s> and </s>, lower case all letters.
def padding_lower(in_file, out_file):
    with open(in_file, "r") as rf:
        with open(out_file, "w") as wf:
            for line in rf:
                wf.write('<s> ' + line.rstrip().lower() + ' </s>' + '\n')

# 2nd preprocessing: 
# train: replace all words with frequency 1 to <unk>.
# test: wrods in test but not in train, replace to <unk>.
def build_unigram_map(file):
    map = {}
    num_tokens = 0
    with open(file, "r") as rf: 
        for line in rf:
            for word in line.split():
                map[word] = map.get(word,0)+1
                num_tokens += 1 
    return map, num_tokens
    # print(f"Num of tokens in training data, repeated: {num_tokens}")
    # print(f"Total unique word types in training data, before <unk>: {len(map)}")

def precetage_in_test_not_train_types(map_train, map_test):
    # counting unique word types.
    count = 0
    for key in map_test.keys():
        if key not in map_train.keys():
            count += 1
    return count

def precetage_in_test_not_train_tokens(map_train, file):
    count_tokens = 0
    keys = map_train.keys()
    with open(file, "r") as rf:
        for line in rf:
            for word in line.split():
                if word not in keys:
                    count_tokens += 1
    return count_tokens

def precetage_in_test_not_train_tokens_bigram(map_train, file):
    count = 0
    keys = map_train.keys()
    with open(file, "r") as rf:
        for line in rf:
            token_list = line.split()
            for i in range(0, len(token_list)-1):
                k_test = token_list[i]+ " " + token_list[i+1]
                if k_test not in keys:
                    count += 1
    return count

def replace_unk_in_map(map):
    unk = []
    for k, v in map.items():
        if v==1:
            unk.append(k)
    # remove key from map  
    for i in unk:
        del map[i]
    print (f"Count of words with frequency 1: {len(unk)}")
    # add <unk> in the map
    map['<unk>'] = len(unk)
    # print (f"Total unique word types in training data, after replaced to <unk>: {len(map)}")

def replace_unk(in_file, out_file, map_train):
    with open(in_file, "r") as rf:
        with open(out_file, "w") as wf:
            for line in rf:
                for word in line.split():
                    if word not in map_train: 
                        wf.write("<unk> ")
                    elif word == "</s>":
                        wf.write("</s>" + "\n")
                    else:
                        wf.write(word+ " ")                                   

def build_bigram_map(file):
    map = {}
    num_tokens = 0
    with open(file, "r") as rf:
        for line in rf:
            token_list = line.split()
            for i in range(0, len(token_list)-1):
                key = token_list[i]+ " " + token_list[i+1]
                map[key] = map.get(key, 0) + 1
                num_tokens += 1
    return map, num_tokens

def MLE_unigram_logp(s, map_train, num_tokens_train):
    sum_logp = 0
    for w in s:
        count_w = (0 if map_train.get(w) == None else map_train.get(w))
        # print(count_w)
        logp = math.log2(count_w / num_tokens_train)
        print(f"[ {w} ] : {logp}")
        sum_logp += logp  
    return sum_logp

def MLE_unigram_logp_test(file, map_train, num_tokens_train):
    sum_logp = 0
    undefined = False 
    with open(file, "r") as rf:
        for line in rf:
            for w in line.split():
                if w != '<s>':
                    count_w = (0 if map_train.get(w) == None else map_train.get(w))
                    p = count_w / num_tokens_train
                    logp = 0 if p == 0.0 else math.log2(p)
                    if logp==0:
                        undefined = True
                    sum_logp += logp
    return 'undefined' if undefined else sum_logp

def MLE_bigram_logp(s, map_train, map_train_bigram, one, v):
    sum_logp = 0
    undefined = False 
    # print(len(s)-1)
    for i in range(0, len(s)-1):
        bigram_key = s[i] + " " + s[i+1]
        c_w_bi = (0 if map_train_bigram.get(bigram_key) == None else map_train_bigram.get(bigram_key)) + one
        c_w = (map_train.get('<unk>') if map_train.get(s[i+1]) == None else map_train.get(s[i])) + v
        p = c_w_bi / c_w
        logp = 0 if p == 0.0 else math.log2(p)
        if logp==0:
            undefined = True
        print(f"[{bigram_key}] : {'undefined' if logp==0 else logp}")
        sum_logp += logp
    return 'undefined' if undefined else sum_logp

def MLE_bigram_logp_test(file, map_train, map_train_bigram, one, v):
    sum_logp = 0
    undefined = False 
    with open(file, "r") as rf:
        for line in rf:
            s = line.split() # token list in one line
            for i in range(0, len(s)-1):
                bigram_key = s[i] + " " + s[i+1]
                c_w_bi = (0 if map_train_bigram.get(bigram_key) == None else map_train_bigram.get(bigram_key)) + one
                c_w = (map_train.get('<unk>') if map_train.get(s[i+1]) == None else map_train.get(s[i])) + v
                p = c_w_bi / c_w
                logp = 0 if p == 0.0 else math.log2(p)
                if logp==0:
                    undefined = True
                # print(f"[{bigram_key}] : {'undefined' if logp==0 else logp}")
                sum_logp += logp
    return 'undefined' if undefined else sum_logp

def perplexity(m, logp, name):
    if logp == 'undefined':
        print(f"Perplexity for {name} : undefined.")
        return 'undefined'
    pp = math.pow(2, logp / m * -1)
    print(f"Perplexity for {name} : {pp}")
    return pp

def main():   
    file_train = sys.argv[1]
    file_test = sys.argv[2]
    # # 1st preprocessing: padding with <s> and </s>, lower case all letters.
    padding_lower(file_train, "train_preprocessed_1.txt")
    padding_lower(file_test, "test_preprocessed_1.txt")
    
    # # build frequency map for both data set.
    # count number of tokens in both data set, repeated.
    map_train, num_tokens_train = build_unigram_map("train_preprocessed_1.txt")
    map_test, num_tokens_test = build_unigram_map("test_preprocessed_1.txt")
    print("Q2----------------------")
    print(f"Total word tokens (repeated) in the training corpus after padding: {num_tokens_train}") # 2568210
    print(num_tokens_test) # 2869
    print(f"number of word token in training before replace to <unk> : { len(map_train) }") # 83045
    print(f"number of word types (unique) in training before replace to <unk> : {len(map_test)}\n") # 1249

    # # Q3, before replace unk
    print("Q3--------- before <unk> -------------")
    np_unique = precetage_in_test_not_train_types(map_train, map_test)
    print(f"Percentage of word Types in test corpus that did not occur in training: {np_unique} / {len(map_test)}")
    np_repeat = precetage_in_test_not_train_tokens(map_train, "test_preprocessed_1.txt")
    print(f"Percentage of word Tokens in test corpus that did not occur in training: {np_repeat} / {num_tokens_test}\n")
    
    # # 2nd preprocessing: 
    # train: replace all words with frequency 1 to <unk>.
    # test: wrods in test but not in train, replace to <unk>.
    replace_unk_in_map(map_train)
    print('\n')
    print("Q1----------------------")
    print(f"Total unique word types in training corpus after padding with <s> and </s>, and replaced to <unk> : {len(map_train)}") # 41739
    replace_unk("train_preprocessed_1.txt", "train_preprocessed_2.txt", map_train)
    replace_unk("test_preprocessed_1.txt", "test_preprocessed_2.txt", map_train)
    map_test, num_tokens_test = build_unigram_map("test_preprocessed_2.txt") 
    print(f"number of word types in test data after replace to <unk> : {len(map_test)}") # 1175
    print(f"number of word tokens in test data after replace to <unk> : {num_tokens_test}\n") # 2869
    # done preprocessing

    # # Q4 Bigrams 
    print("Q4--------- after <unk> -------------")
    map_train_bigram, num_tokens_train_bigram = build_bigram_map("train_preprocessed_2.txt")
    map_test_bigram, num_tokens_test_bigram = build_bigram_map("test_preprocessed_2.txt")

    # print(num_tokens_train_bigram) # 2468210
    # print(num_tokens_test_bigram) # 2769
    # print(len(map_train_bigram)) # 742294
    # print(len(map_test_bigram)) # 2365
    # # np -> not present
    np_unique_bigram = precetage_in_test_not_train_types(map_train_bigram, map_test_bigram)
    print(f"Percentage of word Types in test corpus that did not occur in training: {np_unique_bigram} / {len(map_test_bigram)}")
    np_repeat_bigram = precetage_in_test_not_train_tokens_bigram(map_train_bigram, "test_preprocessed_2.txt")
    print(f"Percentage of word Tokens in test corpus that did not occur in training: {np_repeat_bigram} / {num_tokens_test_bigram}\n")

    # # Q5
    print("Q5----------------------")
    print("Unigram")
    s = ['i', 'look', 'forward', 'to', 'hearing', 'your', 'reply', '.', '</s>']
    log_p_unigram = MLE_unigram_logp(s, map_train, num_tokens_train-100000)
    print(f"Log Probability for Unigram : {log_p_unigram}\n")
    
    print("Bigram")
    sp = ['<s>', 'i', 'look', 'forward', 'to', 'hearing', 'your', 'reply', '.', '</s>']   
    log_p_bigram = MLE_bigram_logp(sp, map_train, map_train_bigram, 0, 0)
    print(f"Log Probability for Bigram : {log_p_bigram}\n")

    print("Bigram Add 1")
    log_p_bigram_add_1 = MLE_bigram_logp(sp, map_train, map_train_bigram, 1, len(map_train))
    print(f"Log Probability for Bigram with Add 1 Smoothing: {log_p_bigram_add_1}\n")

    # # Q6
    print("Q6----------------------")
    s_token = 9
    perplexity(s_token, log_p_unigram, "Unigram")
    perplexity(s_token, log_p_bigram, "Bigram")
    perplexity(s_token, log_p_bigram_add_1, "Bigram Add 1")
    print("\n")

    # # Q7
    print("Q7----------------------")

    load_file = "test_preprocessed_2.txt"
    log_p_unigram_test = MLE_unigram_logp_test(load_file, map_train, num_tokens_train-100000)
    print(f"Log Probability for Unigram in test data : {log_p_unigram_test}")
    perplexity(num_tokens_test_bigram, log_p_unigram_test, "Unigram")
    print("\n")

    log_p_bigram_test = MLE_bigram_logp_test(load_file, map_train, map_train_bigram, 0, 0)
    print(f"Log Probability for Bigram in test data : {log_p_bigram_test}")
    perplexity(num_tokens_test_bigram, log_p_bigram_test, "Bigram")
    print("\n")

    log_p_bigram_add_1_test = MLE_bigram_logp_test(load_file, map_train, map_train_bigram, 1, len(map_train))
    print(f"Log Probability for Bigram with Add 1 Smoothing in test data: {log_p_bigram_add_1_test}")
    perplexity(num_tokens_test_bigram, log_p_bigram_add_1_test, "Bigram Add 1")
    print("\n")

if __name__ == "__main__":
    main()