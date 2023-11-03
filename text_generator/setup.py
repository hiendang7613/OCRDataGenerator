#download load file from url https://huggingface.co/vinai/phobert-large/raw/main/vocab.txt
import urllib.request
url = "https://huggingface.co/vinai/phobert-large/raw/main/vocab.txt"
filename = "vocab.txt"

# urllib.request.urlretrieve(url, filename)

# filename = "vocab.txt"

# with open(filename, "r", encoding="utf-8") as f:
#     vocab = f.readlines()

# vocab = [word.strip().split()[0].replace('_',' ').replace('@','') for word in vocab]


# print(vocab[1640:1690])

import os
import random

# Choose a random file from the list

# Open the file and read a random line
with open(os.path.join(folder_path, random_file), "r", encoding="utf-8") as f:
    lines = [line.rstrip() for line in f.readlines()]
    loop = True
    while loop:
        random_line = random.choice(lines)
        if len(random_line) !=0 and '==' not in random_line:
            loop = False

def get_len():
    return max(0, min(200, round(random.gauss(64, 32))))    

print(len(random_line))
def random_crop(text, length):
    if len(text) <= length:
        return text
    start = random.randint(0, len(text) - length)
    cropped_text = text[start:start+length]
    return cropped_text

text = random_crop(random_line, get_len())
print(text)