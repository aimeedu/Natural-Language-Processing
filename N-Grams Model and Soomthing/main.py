# hw1
# 1st preprocessing: padding with <s> and </s>, lower case all letters.
def padding_lower(in_file, out_file):
    with open(in_file, "r") as rf:
        with open(out_file, "w") as wf:
            for line in rf:
                wf.write('<s> ' + line.rstrip().lower() + ' </s>' + '\n')

# 2nd preprocessing: 
# train: replace all words with frequency 1 to <unk>.
# test: wrods in test but not in train, replace to <unk>.
def build_freq_map(map, file):
    num_tokens = 0
    with open(file, "r") as rf: 
        for line in rf:
            for word in line.split():
                count = map.get(word,0)
                map[word] = count+1
                num_tokens += 1 
    return num_tokens
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
    print (f"Total unique word types in training data, after replaced to <unk>: {len(map)}")

def replace_unk(in_file, out_file, map):
    with open(in_file, "r") as rf:
        with open(out_file, "w") as wf:
            for line in rf:
                for word in line.split():
                    if word == "</s>":
                        wf.write("</s>" + "\n")
                    elif word in map:
                        wf.write(word+ " ")
                    else:
                        wf.write("<unk> ")

def main():    
    # 1st preprocessing: padding with <s> and </s>, lower case all letters.
    # padding_lower("train.txt", "train_preprocessed_1.txt")
    # padding_lower("test.txt", "test_preprocessed_1.txt")
    
    # build frequency map for both data set.
    map_train = {} 
    map_test = {}
    # count number of tokens in both data set, repeated.
    num_tokens_train = build_freq_map(map_train, "train_preprocessed_1.txt")
    num_tokens_test = build_freq_map(map_test, "test_preprocessed_1.txt")
    
    # print(num_tokens_train)
    # print(num_tokens_test)
    
    # np_unique = precetage_in_test_not_train_types(map_train, map_test)
    # print(f"Percentage of word Types in test corpus that did not occur in training: {np_unique} / {len(map_test)}")

    # np_repeat = precetage_in_test_not_train_tokens(map_train, "test_preprocessed_1.txt")
    # print(f"Percentage of word Tokens in test corpus that did not occur in training: {np_repeat} / {num_tokens_test}")
    
    # 2nd preprocessing: 
    # train: replace all words with frequency 1 to <unk>.
    # test: wrods in test but not in train, replace to <unk>.
    replace_unk("train_preprocessed_1.txt", "train_preprocessed_2.txt", map_train)
    replace_unk("test_preprocessed_1.txt", "test_preprocessed_2.txt", map_test)

    # done with preprocessing


if __name__ == "__main__":
    main()