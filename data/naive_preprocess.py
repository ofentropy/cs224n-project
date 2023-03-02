import re

def normalize(raw: str):
    return re.sub(r"[^A-Za-z0-9 ']+", "", raw.lower())

fluent = input("Input fluent sentence: ")

# remove punctuation except for apostrophes
fluent_arr = normalize(fluent).split()
fluent_dict = {}
for i, word in enumerate(fluent_arr):
    fluent_dict[i] = word

print(fluent_dict)