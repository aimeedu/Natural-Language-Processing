import gzip
import gensim
import logging
import os
import bz2

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)


def show_file_contents(input_file):
    with bz2.open(input_file, 'rb') as f:
        for i, line in enumerate(f):
            print(line)
            break


def read_input(input_file):
    """This method reads the input file which is in gzip format"""

    logging.info("reading file {0}...this may take a while".format(input_file))
    with bz2.open(input_file, 'rb') as f:
        for i, line in enumerate(f):

            if (i % 10000 == 0):
                logging.info("read {0} reviews".format(i))
            # do some pre-processing and return list of words for each review
            # text
            yield gensim.utils.simple_preprocess(line)


if __name__ == '__main__':

    # data_file = "news.crawl.bz2"
    abspath = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(abspath, "../news.crawl.bz2")

    # read the tokenized reviews into a list
    # each review item becomes a serries of words
    # so this becomes a list of lists
    # documents = list(read_input(data_file))
    documents = list(read_input("news.crawl.bz2"))
    logging.info("Done reading data file")

    # build vocabulary and train model
    model = gensim.models.Word2Vec(
        documents,
        vector_size=50,
        window=2,
        min_count=2,
        workers=10)
    model.train(documents, total_examples=len(documents), epochs=10)

    # save only the word vectors
    # model.wv.save(os.path.join(abspath, "../vectors/default"))
    model.wv.save("word2vec.model")

    w1 = "dirty"
    print("Most similar to {0}".format(w1), model.wv.most_similar(positive=w1))

    # look up top 5 words similar to 'polite'
    w1 = ["polite"]
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=5))

    # look up top 5 words similar to 'orange'
    w1 = ["orange"]
    print(
        "Most similar to {0}".format(w1),
        model.wv.most_similar(
            positive=w1,
            topn=5))

    # # get everything related to stuff on the bed
    # w1 = ["bed", 'sheet', 'pillow']
    # w2 = ['couch']
    # print(
    #     "Most similar to {0}".format(w1),
    #     model.wv.most_similar(
    #         positive=w1,
    #         negative=w2,
    #         topn=10))

    # similarity between two different words
    print("Similarity between 'dirty' and 'clean'",
          model.wv.similarity(w1="dirty", w2="clean"))

    # similarity between two identical words
    print("Similarity between 'big' and 'dirty'",
          model.wv.similarity(w1="big", w2="dirty"))

    # similarity between two unrelated words
    print("Similarity between 'big' and 'large'",
          model.wv.similarity(w1="big", w2="large"))

    # similarity between two unrelated words
    print("Similarity between 'big' and 'small'",
          model.wv.similarity(w1="big", w2="small"))