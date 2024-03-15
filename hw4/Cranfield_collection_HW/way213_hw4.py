import numpy as np
from collections import Counter, defaultdict
import re
from stop_list import closed_class_stop_words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# PART 1 ---------------------------------------------------------------------------------------------------------------------
# filed downloaded and unzipped

# PART 2 - QUERIES AND ANSWER KEY --------------------------------------------------------------------------------------------------------------------

# open files:
with open('cran.qry', 'r') as f:
    cran_qry_items = f.read()

with open('cran.all.1400', 'r') as f:
    cran_abs_items = f.read()

# let's first clean text of any stop words, punctuation, and numbers, we'll do this by defining a method

# function to parse the query.
def parse_query(items):
    # make a dictionary to store the queries and their ids
    queries = {}
    current_id = ""

    lines = items.split('\n')
    for line in lines:
        if line.startswith('.I'):
            # get current_id
            current_id = line.split(' ')[1]
            queries[current_id] = ""
        elif line.startswith('.W'):
            continue
        else:
            queries[current_id] += line + " "
    return queries

# function to parse the abstract file
def parse_cran_abstracts(content):
    abstracts = {}
    current_id = ""
    lines = content.split('\n')
    in_abstract = False
    for line in lines:
        if line.startswith('.I'):
            current_id = line.split(' ')[1]
            in_abstract = False
        elif line.startswith('.W'):
            in_abstract = True
            abstracts[current_id] = ""
        elif in_abstract:
            abstracts[current_id] += line + " "
    return abstracts

query_dict = parse_query(cran_qry_items)
abstracts_dict = parse_cran_abstracts(cran_abs_items)



# now we can make a function to actually remove the stop words and all other irrelevant text
# this function will only clean one line of text at a time


def clean_one_line_of_text(query):
    # Remove numbers and punctuation
    cleaned_query = re.sub(r'[^\w\s]', '', query)
    cleaned_query = re.sub(r'\d+', '', cleaned_query)
    
    # Split text into words
    words = cleaned_query.split()
    
    # Remove stop words
    filtered_words = [word for word in words if word.lower() not in closed_class_stop_words]
    
    # Rejoin words into a string
    result = ' '.join(filtered_words)

    # stemming 
    
    return result

# - for every single key within the dictionary
for i in query_dict.keys():
    # overwrite the query with the newly parsed query
    query_dict[i] = clean_one_line_of_text(query_dict[i])

for i in abstracts_dict.keys():
    # overwrite the text with the newly parsed text
    abstracts_dict[i] = clean_one_line_of_text(abstracts_dict[i])



# GREAT --------------------------------------------------------------------------------------------------------------------
# we are now done with cleaning the query and abstraction data

def calculate_idf_scores(tokenized_corpus):
    word_document_freq = defaultdict(int)
    total_documents = len(tokenized_corpus)

    # Count document frequency for each word
    for doc in tokenized_corpus:
        unique_words = set(doc)
        for word in unique_words:
            word_document_freq[word] += 1

    # Calculate IDF scores
    idfs = {word: np.log(total_documents / (1 + freq)) for word, freq in word_document_freq.items()}
    return idfs

# IDF scores for queries and abstracts
idfs_queries = calculate_idf_scores(query_dict.values())
idfs_abstracts = calculate_idf_scores(abstracts_dict.values())


# function to calculate TF-IDF scores using precomputed IDF scores
def calculate_tfidf_scores(tokenized_data, idfs):
    tfidf_scores = {}
    for key, tokens in tokenized_data.items():
        # Task : Count the number of instances of each non-stop-word in each query
        # Count term frequency
        term_counts = Counter(tokens)
        total_terms = len(tokens)

        # Calculate TF-IDF scores
        # Task : Vector lists the TF-IDF scores for the words in the vector
        tf_scores = {term: count / total_terms for term, count in term_counts.items()}
        tfidf_scores[key] = {term: tf_scores[term] * idfs.get(term, 0) for term in tf_scores}
    
    return tfidf_scores

tfidf_scores_queries = calculate_tfidf_scores(query_dict, idfs_queries)
tfidf_scores_abstracts = calculate_tfidf_scores(abstracts_dict, idfs_abstracts)
# calculate TF-IDF scores for each query
tfidf_scores = calculate_tfidf_scores(query_dict, idfs_queries)

# function to count word frequencies in each abstract
def count_word_frequencies(abstracts_tokenized):
    word_frequencies = {}
    for doc_id, tokens in abstracts_tokenized.items():
        word_counts = defaultdict(int)
        for token in tokens:
            word_counts[token] += 1
        word_frequencies[doc_id] = dict(word_counts)
    return word_frequencies

# Count the word frequencies in each abstract
word_frequencies_abstracts = count_word_frequencies(abstracts_dict)

# Convert tokenized queries and abstracts back to string format for TF-IDF vectorization
queries_str = [" ".join(tokens) for tokens in query_dict.values()] # For each query
abstracts_str = [" ".join(tokens) for tokens in abstracts_dict.values()] # For each abstract

# Combine queries and abstracts for TF-IDF vectorization (to ensure vocabulary matches)
combined_texts = list(query_dict.values()) + list(abstracts_dict.values())

# Initialize and fit TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(combined_texts)

# Split TF-IDF matrix back into queries and abstracts
tfidf_queries = tfidf_matrix[:len(queries_str)]
tfidf_abstracts = tfidf_matrix[len(queries_str):]

# Compute cosine similarity between each query and all abstracts
cosine_similarities = cosine_similarity(tfidf_queries, tfidf_abstracts)
        
output_lines = []

# Iterate over each query's cosine similarities with abstracts
for query_index, similarities in enumerate(cosine_similarities):
    # Sort the indices of abstracts based on similarity scores in descending order
    sorted_indices = np.argsort(similarities)[::-1]
    # Filter out indices where similarity score is 0, but ensure at least 100
    non_zero_indices = [index for index in sorted_indices if similarities[index] > 0]
    
    # Iterate over filtered and possibly extended indices to prepare lines for the output file
    for rank, abstract_index in enumerate(non_zero_indices):
        # Format : query_id, abstract_id, cosine_similarity_score
        line = f"{query_index + 1} {abstract_index + 1} {similarities[abstract_index]:.12f}"
        output_lines.append(line)


output_file_path = 'output.txt'
with open(output_file_path, 'w') as file:
    # Write each line to the file
    for line in output_lines:
        file.write(line + '\n')  # Each entry appears on a new line