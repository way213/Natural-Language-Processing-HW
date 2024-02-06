import re

def find_dollar_amounts(text):
    dollar_regex = r"""
        # Matches $ amounts with optional million or billion

        # matches $, captures up to 3 digits after the $
        (
            \$\d{1,3}  
            # OPTIONAL - matches exactly 3 digits after commas up to any amount of times with '*' 
            (?:,\d{3})*
            # OPTIONAL - matches up to 2 digiths after a decimal point ONCE.
            (?:\.\d{1,2})?
            # OPTIONAL - matches any amount of white spaces 
            \s*
            # OPTIONAL - matches million or billions ONCE w/ 'b'
            (?:million|billion)?\b)|


            # Matches numerical dollar amounts possibly followed by "and" cents
            (\d{1,3}(?:,\d{3})*
            (?:\.\d{1,2})?
            \s*
            (?:dollar|dollars)\s*
            (and\s*\d{1,2}\s*
            (cent|cents))?)|
            
            # Matches simple $ amounts with optional decimals
            (\$\d{1,3}
            (?:,\d{3})*
            (?:\.\d{1,2})?|


            # Matches some 'words' of numbers
            \b(?:a|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty)\s+dollars\b
        )
    """
    matches = re.findall(dollar_regex, text, re.IGNORECASE | re.VERBOSE)
    print(matches[:10])
    cleaned_matches = ["".join(match).replace('\n', ' ').strip() for match in matches if any(match)]
    return cleaned_matches

# read from a file
input_file_path = 'regexp_corpora/test_dollar_phone_corpus.txt'
with open(input_file_path, 'r', encoding='utf-8') as file:
    text_to_search = file.read()

# find matches
matches = find_dollar_amounts(text_to_search)

# write matches to a file
output_file_path = 'results/dollar_output.txt'  
with open(output_file_path, 'w') as file:
    for match in matches:
        file.write(match + '\n')

print(f"Matches written to {output_file_path}. Total matches found: {len(matches)}")
