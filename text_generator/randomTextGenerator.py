import random
import string
import re

english_characters = list(string.ascii_lowercase)
vietnamese_characters = list("áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ")
punctuation_characters = string.punctuation 


class RandomCharGenerator:
    def __init__(self):
        self.p_char = 0.7
        self.p_upper = 0.5
        self.p_eng = 0.7
        self.engList = english_characters
        self.notengList = vietnamese_characters

        self.p_punc = 0.1
        self.puncList = punctuation_characters

        self.p_sp = 0.2
    
    def __get_rand_char(self):
        # random upper or lower
        if random.random() < self.p_eng:
            charList = self.engList
        else:
            charList = self.notengList
        char = charList[random.randint(0, len(charList) - 1)]
        return char.upper() if random.random() < self.p_upper else char

    def __get_rand_punc(self):
        return self.puncList[random.randint(0, len(self.puncList) - 1)]

    def generate(self):
        # random character by probability
        if random.random() < self.p_char:
            return self.__get_rand_char()
        elif random.random() < self.p_char + self.p_punc:
            return self.__get_rand_punc()
        else:
            return ' '

    # random number from 0 to 256 by gaussian distribution with mean = 64 and std = 32
    def __get_len(self):
        return max(0, min(256, round(random.gauss(64, 32))))    
    
    def get_string(self):
        string_len = self.__get_len()
        string = ''.join([self.generate() for _ in range(string_len)])
        string = re.sub(r'\s{2,}', ' ', string)
        return string

# read vocab.txt
filename = "vocab.txt"
with open(filename, "r", encoding="utf-8") as f:
    vocab = f.readlines()
vocab = [word.strip().split()[0].replace('_',' ').replace('@','') for word in vocab]


class RandomWordGenerator:
    def __init__(self):
        self.p_upper = 0.5
        self.p_first_upper = 0.5
        self.p_all_upper = 0.4
        self.p_rand_upper = 0.1
        self.vocab = vocab

        self.p_punc = 0.2
        self.puncList = punctuation_characters

    
    def __get_rand_word(self):
        word = self.vocab[random.randint(0, len(self.vocab) - 1)]
        # random upper or lower
        if random.random() < self.p_upper:
            if random.random() < self.p_first_upper:
                word = word[0].upper() + word[1:]
            elif random.random() < self.p_first_upper + self.p_all_upper:
                word = word.upper()
            elif random.random() < self.p_first_upper + self.p_all_upper + self.p_rand_upper:
                word = ''.join([char.upper() if random.random() < self.p_upper else char for char in word])
        return word

    def __get_rand_punc(self):
        return self.puncList[random.randint(0, len(self.puncList) - 1)]

    def __get_len(self):
        return max(0, min(256, round(random.gauss(64, 32))))    
    
    def get_string(self):
        string_len = self.__get_len()
        string = ''
        while len(string) < string_len:
            punc1 = self.__get_rand_punc() if random.random() < self.p_punc else ''
            punc2 = self.__get_rand_punc() if random.random() < self.p_punc else ''
            string += self.__get_rand_word() + punc1 + ' ' + punc2
        string = string[:string_len].strip()
        return string

import os
class RandomSentenceWikiGenerator:
    def __init__(self, wiki_path='./viwiki'):
        self.wiki_path = wiki_path
        self.file_list = os.listdir(wiki_path)
        self.max_len = 200

    def __get_len(self):
        return max(0, min(self.max_len, round(random.gauss(64, 32))))    

    def __random_crop(self, text, length):
        if len(text) <= length:
            return text
        start = random.randint(0, len(text) - length)
        cropped_text = text[start:start+length]
        return cropped_text

    def get_string(self):
        random_file = random.choice(self.file_list)

        with open(os.path.join(self.wiki_path, random_file), "r", encoding="utf-8") as f:
            lines = [line.rstrip() for line in f.readlines()]
            loop = True
            while loop:
                random_line = random.choice(lines)
                if len(random_line) !=0 and '==' not in random_line:
                    loop = False
        text = self.__random_crop(random_line, self.__get_len())
        return text


#test
if __name__ == "__main__":
    # randomchar = RandomCharGenerator()
    # print(randomchar.get_string())
    # randomword = RandomWordGenerator()
    # print(randomword.get_string())
    randomwiki = RandomSentenceWikiGenerator()
    print(randomwiki.get_string())