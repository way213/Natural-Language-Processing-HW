import re

def find_phone_numbers(text):
    phone_regex = r"""
    # area code is in parenthesis
    (?:\(\d{3}\)(?:\s|-|.)\d{3}(?:\s|-|.)\d{4}\b)|
    # area code is NOT in parenthesis
    (?:\d{3}(?:\s|-|.)\d{3}(?:\s|-|.)\d{4}\b)|
    # simply nine numbers no spaces
    \b(?:\d{9})\b|
"""


    matches = re.findall(phone_regex, text, re.VERBOSE)
    print(matches[:10])
    cleaned_matches = ["".join(match).replace('\n', ' ').strip() for match in matches if any(match)]
    return cleaned_matches

# read from a file
input_file_path = 'regexp_corpora/test_dollar_phone_corpus.txt'
with open(input_file_path, 'r', encoding='utf-8') as file:
    text_to_search = file.read()

# find matches
matches = find_phone_numbers(text_to_search)

# write matches to a file
output_file_path = 'results/telephone_output.txt'  
with open(output_file_path, 'w') as file:
    for match in matches:
        file.write(match + '\n')

print(f"Matches written to {output_file_path}. Total matches found: {len(matches)}")
