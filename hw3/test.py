keyFileName = 'data/WSJ_24.pos'
responseFileName = 'data/WSJ_02-21.pos'

# Assuming the score module is correctly imported and used elsewhere
from hw3.score import score


def merge_data(file1, file2):
	# Name of the newly merged file
	new_file = 'merged_training_set.pos'

	# Append content from the first file
	with open(responseFileName, 'r', encoding='utf8') as csv_file:
		with open(new_file, "w", encoding='utf8') as merged_file:
			for line in csv_file:
				merged_file.write(line)

	# Append content from the second file
	with open(keyFileName, 'r', encoding='utf8') as payload:
		with open(new_file, "a", encoding='utf8') as merged_file:  # Use append mode here
			for line in payload:
				merged_file.write(line)
	return new_file