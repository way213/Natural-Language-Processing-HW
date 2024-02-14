To run the system, please follow the following steps:


1. Make sure that the test data (WSJ_02-21.pos, WSJ_24.pos), testing data (WSJ_23.pos) as well as the scoring file provided to us (score.py) are within the same directory as our program (way213_viterbi_HW3.py)


2. Now you are set to run the program, simply run way213_viterbi_HW3.py.


3. The program merges the two assigned test datasets as indicated above into a file named merged_training_set.pos.


4. The result of the program will be stored in the file submissions.pos


5. Please note that if you would like to re-run the program, you are required to delete the newly created files, both merged_training_set.pos and submissions.pos


6. There is a commented out block at the very end to check scores of the file created IF the correct results are , please use accordngly.


The way that I decided to handle OOV words was to use a constant of 1e-10 as the likelihood for all OOV items -- effectively only using the transition probability for OOV words while not crashing the program either.