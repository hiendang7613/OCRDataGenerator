import ast
import random
import os

class RandomFontGenerator:
    def __init__(self, font_dir):
        self.font_set=[]
        for root, _, files in os.walk(font_dir):
            for file in files:
                if file.endswith(".ttf"):
                    self.font_set.append(os.path.join(root, file))

    def get_font_path(self):
        # print(self.font_set)
        font = self.font_set[random.randint(0, len(self.font_set) - 1)]
        return font

