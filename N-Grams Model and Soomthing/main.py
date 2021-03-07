# hw1

# with open("train.txt", "r") as rf:
#     with open("train_preprocessed.txt", "w") as wf:
#     # # return each line in a list, ready for preprocessing
#     # before = f.readlines() 
#     # print(before[3])
#         for line in rf:
#             wf.write('<s> ' + line.rstrip().lower() + ' </s>' + '\n')

# frequency map
map = {}
sum = 0
with open("train_preprocessed.txt", "r") as wf:
    for line in wf:
        for word in line.split():
            count = map.get(word,0)
            map[word] = count+1
            sum = sum+1

print(sum)
print(len(map))

unk = []
for k, v in map.items():
    if v==1:
        unk.append(k)

# remove key from map  
for i in unk:
    del map[i]

print (len(unk))
# add <unk> in the map
map['<unk>'] = len(unk)
print (len(map))


