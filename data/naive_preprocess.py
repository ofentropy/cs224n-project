import re
import csv
from data.keys import *
from nltk import pos_tag # requires nltk install

def normalize(raw: str):
    return re.sub(r"[^A-Za-z0-9 ']+", "", raw.lower())

def get_indices():
    fluent = input("Input fluent sentence: ")

    # remove punctuation except for apostrophes
    fluent_arr = normalize(fluent).split()
    fluent_dict = {}
    for i, word in enumerate(fluent_arr):
        fluent_dict[i] = word

    print(fluent_dict)

def get_nltk_pos_tags(load_path: str, save_path: str):
    temp = []

    with open(load_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            temp.append(row)

    with open(save_path, 'w', newline='') as csv_file:
        fieldnames = list(temp[0].keys()) + ["pos_tags"]
        writer = csv.DictWriter(csv_file, fieldnames)
        writer.writeheader()
        for row in temp:
            disfluent = row["disfluent_sentence"].split()
            raw = pos_tag(disfluent)
            temp_2 = []
            pos_tags = [r[1] for r in raw]
            row["pos_tags"] = pos_tags
            writer.writerow(row)


def convert_csv_to_txt(load_path: str, save_path: str, order_save_path = None):
    temp = []
    valid = []

    with open(load_path, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            temp.append(row)

    with open(save_path, 'w', newline='') as txt_file:
        for row in temp:
            disfluent = "\t".join(row["disfluent_sentence"].split())
            pos_tags = "\t".join(row["pos_tags"].split())
            io = "\t".join(row["io_indexing"].split())

            if disfluent:
                valid.append(row)
            txt_file.write(disfluent)
            txt_file.write('\n')
            txt_file.write(pos_tags)
            txt_file.write('\n')
            txt_file.write(io)
            txt_file.write('\n')
            txt_file.write('\n')
    
    if order_save_path:
        with open(order_save_path, 'w', newline='') as txt_file:
            for row in valid:
                txt_file.write(row["id"])
                txt_file.write("\n")
    return valid
        