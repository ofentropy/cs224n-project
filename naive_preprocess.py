import re

fluent = input("Input fluent sentence: ")

# remove punctuation except for apostrophes
fluent_arr = (re.sub(r"[^A-Za-z0-9 ']+", "", fluent)).split()
fluent_dict = {}
for i, word in enumerate(fluent_arr):
    fluent_dict[i] = word

print(fluent_dict)