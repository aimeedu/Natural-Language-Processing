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
def build_freq(map, total):
    with open("train_preprocessed_1.txt", "r") as rf: 
        for line in rf:
            for word in line.split():
                count = map.get(word,0)
                map[word] = count+1
                total = total+1 
    print(f"total words in training data, repeated: {total}")
    print(f"total unique words in training data, before <unk>: {len(map)}")

    unk = []
    for k, v in map.items():
        if v==1:
            unk.append(k)

    # remove key from map  
    for i in unk:
        del map[i]

    print (f"count of words with frequency 1: {len(unk)}")
    # add <unk> in the map
    map['<unk>'] = len(unk)
    print (f"total unique words in training data after replaced to <unk>: {len(map)}")


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
    # frequency map for training data.
    map = {} 
    # total words in training data, repeated.
    total = 0 
    build_freq(map, total)

    # 1st preprocessing: padding with <s> and </s>, lower case all letters.
    # padding_lower("train.txt", "train_preprocessed_1.txt")
    # padding_lower("test.txt", "test_preprocessed_1.txt")
    
    # 2nd preprocessing: 
    # train: replace all words with frequency 1 to <unk>.
    # test: wrods in test but not in train, replace to <unk>.
    # replace_unk("train_preprocessed_1.txt", "train_preprocessed_2.txt", map)
    # replace_unk("test_preprocessed_1.txt", "test_preprocessed_2.txt", map)

if __name__ == "__main__":
    main()