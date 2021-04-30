Run Time of the program is 11.28s for first training 25,000 IMDB movie reviews, then testing another 25,000 IMDB movie reviews.
Overall testing accuracy is 81.45599999999999% for 25,000 IMDB movie reviews.

Before running the program:
Navigate to the working directly which contains all the files needed, main.py, train, test,imdb.vocab, etc. 
The working directory should be generated automatically for the pre-processing, tested on mac os.
Please run this project using the following command, with all the input files in the same directory:
python3 main.py 

The training and testing data should have the following structure:
train and test folder should place in the same directory with main.py.
the class should have proper name, it's the label given to be classified.

├──main.py
├──pre_process.py
├──NB.py
├──imdb.vocab
├──train 
|    ├── class 1  
|    |     ├── file1.txt 
|    |     |── file2.txt 
|    |     └── file3.txt ...
|    └── class 2
|          ├── file1.txt 
|          |── file2.txt 
|          └── file3.txt ...
└──test 
    ├── class 1  
    |     ├── file1.txt 
    |     |── file2.txt 
    |     └── file3.txt ...
    └── class 2
          ├── file1.txt 
          |── file2.txt 
          └── file3.txt ...

After running the program:
There will be 2 outputfiles:
1. movie_review_BOW.txt -> this file stores all the training parameters in log probability.
2. output.txt -> this file store the testing result/prediction for each document, and the overall accuracy of the testing. 
