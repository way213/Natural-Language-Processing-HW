import nltk
from nltk.stem import PorterStemmer

# Initialize the stemmer
stemmer = PorterStemmer()

# Helper function to check capitalization
def is_capitalized(word):
    return word[0].isupper()

# Function to preprocess lines from the input files
def preprocess_lines(lines):
    sentences = []
    current_sentence = []

    # Explicitly handle an initial empty line
    if lines and lines[0].strip() == '':
        sentences.append([])  # Add an empty sentence to reflect the initial empty line

    for line in lines:
        if line.strip() == '':
            if current_sentence:
                sentences.append(current_sentence)
                current_sentence = []
        else:
            fields = line.strip().split('\t')
            current_sentence.append(fields)
    if current_sentence:  # Add the last sentence if it exists
        sentences.append(current_sentence)
    return sentences

# Extract features for a single token
def extract_features(sentence, index, is_training):
    word, pos = sentence[index][:2]
    features = [word, pos]  # Keep the original format for word and POS tag
    if index > 0:
        prev_word, prev_pos = sentence[index - 1][:2]
        features.extend([f"prev_word={prev_word}", f"prev_POS={prev_pos}"])
    if index < len(sentence) - 1:
        next_word, next_pos = sentence[index + 1][:2]
        features.extend([f"next_word={next_word}", f"next_POS={next_pos}"])

    feature_line = "\t".join(features)
    if is_training and len(sentence[index]) > 2:
        bio_tag = sentence[index][2]
        feature_line += f"\t{bio_tag}"
    return feature_line

# Function to process a file and generate features
def generate_features(file_path, is_training=True):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    sentences = preprocess_lines(lines)
    feature_lines = []
    for sentence in sentences:
        for index in range(len(sentence)):
            feature_line = extract_features(sentence, index, is_training)
            feature_lines.append(feature_line)
        feature_lines.append("")  # Blank line to separate sentences
    return feature_lines

# Paths to your input files
training_file_path = 'WSJ_02-21.pos-chunk'
development_file_path = 'WSJ_23.pos'

# Generate features
training_features = generate_features(training_file_path, is_training=True)
development_features = generate_features(development_file_path, is_training=False)

# Output paths for the feature files
training_output_path = 'training.feature'
development_output_path = 'test.feature'

# Write the feature lines to the output files
with open(training_output_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(training_features))

with open(development_output_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(development_features))

print("Feature files generated successfully.")
