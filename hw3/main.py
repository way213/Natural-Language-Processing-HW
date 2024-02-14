
# A training file (WSJ_02-21.pos) consisting of about 950K words. Each line consists of a token, a single blank, and the part-of-speech of that token using the Penn Treebank tag set. Sentence boundaries are marked by an empty line (about 40K sentences).
# A Development file (WSJ_24.pos) in the same format as the training file, consisting of about 32.9 K words (about 1350 sentences).
# A Development test file (WSJ_24.words) -- the same as WSJ_24.pos, but without the POS tags

# A Test file (WSJ_23.words) in the same format as the Development test file. (56.7K words, about 2415 sentences.)
# A README.txt file describing the data
# A scoring program (score.py) for you to see how well you are doing on the development set.

# For development purposes, use the development corpus as your test corpus. Use it for debugging and improving your code, initially ignoring the POS. Later when you are ready to submit the HW, merge the development and training corpora. So you can train with more data when running the system you are submitting.
# Make a table of the prior probabilities for each of POS tags (assuming bigrams) using the training corpus. (update your training corpus before submitting as per 2)
# Make a likelihood table including all words in the training corpus. (update your training corpus before submitting as per 2)
# Make a list of all the words that you find in the training corpus. Any word that is not in this list is out of vocabulary (OOV). You may find OOV words when running the system and will have to treat them specially because otherwise they will have a likelihood of 0 for all POS tags.
# Implement a Viterbi HMM POS tagger using the prior probabilities and likelihood tables. This program should take a corpus in the format of the test corpus and produce output in the format of the training corpus. As per 2, in the development stage of your program-writing use the training corpus to create the tables and run the system on the development corpus. For the final system, merge the training and development and run on the test.

import csv
from collections import defaultdict
from data.score import score


# method to merge two files together 
def merge_data(file1, file2):
	# Name of the newly merged file
	new_file = 'merged_training_set.pos'

	# Append content from the first file
	with open(file1, 'r', encoding='utf8') as csv_file:
		with open(new_file, "w", encoding='utf8') as merged_file:
			for line in csv_file:
				merged_file.write(line)

	# Append content from the second file
	with open(file2, 'r', encoding='utf8') as payload:
		with open(new_file, "a", encoding='utf8') as merged_file:  # Use append mode here
			for line in payload:
				merged_file.write(line)
	return new_file
# ------------------------------------------------------------------------------------------------------------------------------------
# development training file --
development_training_file = "data/WSJ_02-21.pos"

# here is the merged training file -- only used for final system.
merged_training_file = merge_data('data/WSJ_02-21.pos', 'data/WSJ_24.pos')

# here is the testing file, should not be changed
testing_file = 'data/WSJ_24.words'
# ------------------------------------------------------------------------------------------------------------------------------------
# Part #3: getting the count of tags for every prior tag.

prior_tags_count = defaultdict(lambda: defaultdict(int))

with open(merged_training_file, 'r', encoding='utf8') as csv_file:
    # initialize the prior tag to 'start'
    prior_tag = 'start'

    for line in csv_file:
        # strip the line first
        line = line.strip()
        if line:
            # Process token and tag
            word, current_tag = line.split()
            # load this into our dictionary... also keeping track of count
            prior_tags_count[prior_tag][current_tag] += 1
            # now the new prior tag is the last tag extracted
            prior_tag = current_tag
        # if there is nothing in 'line' (which means that it is the end of a sentence, reset the prior tag to 'start')
        else:
            prior_tag = 'start'

    # transform the variable 'prior_tags_counts' to hold the probability of each tag - instead of the count of each tag under a prior tag.
    # (dividing total count in each instance to get probability)
                
    for prior_tag, tag_count in prior_tags_count.items():
        total_count = sum(tag_count.values())
        for tag, count in tag_count.items():
            tag_count[tag]=count/total_count
# ------------------------------------------------------------------------------------------------------------------------------------
# Part 4: Create the likelihood table
# Calculates likelihoods by dividing by the total count of the tag
words_and_tags = defaultdict(lambda: defaultdict(int))

with open(merged_training_file, 'r', encoding='utf8') as csv_file:
    for line in csv_file:
        # strip the line first
        line = line.strip()
        if line:
            # Process word and tag
            word, tag = line.split()
            # load this into our dictionary... also keeping track of count
            words_and_tags[tag][word] += 1

    # for each word in each tag, calculate the probability via dividing count of word with total count of words in each tag
    for tag, word_count in words_and_tags.items():
        total_tag_count = sum(word_count.values())
        for word, count in word_count.items():
            word_count[word] = count / total_tag_count

# ------------------------------------------------------------------------------------------------------------------------------------
# Step 5: Generate a set of unique words and tags
# Use a set to store unique words encountered in the training corpus
all_unique_words_in_data=set()
all_unique_tags_in_data=set()

with open(merged_training_file, 'r', encoding='utf8') as csv_file:
    for line in csv_file:
        # strip the line first
        line = line.strip()
        if line:
            try:
                # Process token and tag
                word, tag = line.split()
                # load this into our set
                all_unique_words_in_data.add(word)
                all_unique_tags_in_data.add(tag)
            # if there is nothing to split (which means that it is the end of a sentence)
            except:
                pass

# ------------------------------------------------------------------------------------------------------------------------------------
# Step 6: Implement Viterbi HMM POS tagger
def viterbi(sentence, unique_tags, prior_probabilities, tag_probabilities):
    # Initialization
    V = [{}]
    path = {}

    # Base case: initialize the probabilities for the first word
    for tag in unique_tags:
        # Use a small value for OOV words (1e-10), via .get()
        V[0][tag] = prior_probabilities['start'].get(tag, 0) * tag_probabilities[tag].get(sentence[0], 1e-10) 
        path[tag] = [tag]

    # Run Viterbi for t > 0
    for t in range(1, len(sentence)):
        V.append({})
        newpath = {}

        for current_tag in unique_tags:
            (prob, state) = max((V[t-1][prev_tag] *
                                 prior_probabilities[prev_tag].get(current_tag, 0) *
                                 tag_probabilities[current_tag].get(sentence[t], 1e-10), prev_tag) for prev_tag in unique_tags)

            V[t][current_tag] = prob
            newpath[current_tag] = path[state] + [current_tag]

        path = newpath

    # Find the best path for the last word
    (prob, state) = max((V[len(sentence) - 1][final_tag], final_tag) for final_tag in unique_tags)
    return path[state]

# ------------------------------------------------------------------------------------------------------------------------------------
# Step 7: Passing in real testing data
# now passing in the data and output the result to a file.

with open(testing_file, 'r', encoding='utf8') as csv_file:
    # initialize empty file to store results
    f = open("WSJ_24_RESULTS.pos", "w")
    # initialize empty list to store a sentence
    current_sentence = []

    for line in csv_file:
        # strip the line first
        line = line.strip()

        if line:
            # Process token
            word = line
            # load this into our sentence variable
            current_sentence.append(word)

        # if there is nothing to split (which means that it is an empty line thus the end of a sentence)
        # run the viterbi algo on current sentence
        else:
            result = viterbi(current_sentence, all_unique_tags_in_data, prior_tags_count, words_and_tags)
            # Write each word and its predicted tag to the file
            for word, tag in zip(current_sentence, result):
                f.write(f"{word}\t{tag}\n")
                # Write an empty line to separate sentences
            f.write("\n")
            current_sentence = []

    print('Created results! ')
    f.close()

# now let's see our results with 'score.py'
keyFileName = 'data/WSJ_24.pos'
responseFileName = 'WSJ_24_RESULTS.pos'

score (keyFileName, responseFileName)




