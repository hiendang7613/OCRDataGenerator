import os
import random
import random as rnd
import numpy as np
from torchvision.transforms import v2
from typing import Tuple
from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageStat
from background_generator.randombackground import RandomBackground
from PIL import Image, ImageOps

def get_text_height(image_font: ImageFont, text: str) -> int:
    return image_font.getbbox(text)[3]

def get_char_width(image_font, character):
    return round(image_font.getlength(character))

def _generate_horizontal_text(
    text: str,
    font: str,
    text_color: str,
    font_size: int,
    word_space_scale: int,
    char_space_scale: int,
    stroke_width: int = 0,
    stroke_fill: str = "#282828",
) -> Tuple:
    word_split=False

    image_font = ImageFont.truetype(font=font, size=font_size)
    space_width = int(get_char_width(image_font, " ") * word_space_scale)
    list_widths = [get_char_width(image_font, p) if p != " " else space_width for p in text]
    text_width = sum(list_widths)
    text_width += int(char_space_scale * (len(text) - 1))
    text_height = max([get_text_height(image_font, p) for p in text])
    txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    txt_img_draw = ImageDraw.Draw(txt_img)
    colors = [ImageColor.getrgb(c) for c in text_color.split(",")]
    c1, c2 = colors[0], colors[-1]
    fill = (
        rnd.randint(min(c1[0], c2[0]), max(c1[0], c2[0])),
        rnd.randint(min(c1[1], c2[1]), max(c1[1], c2[1])),
        rnd.randint(min(c1[2], c2[2]), max(c1[2], c2[2])),
    )
    stroke_colors = [ImageColor.getrgb(c) for c in stroke_fill.split(",")]
    stroke_c1, stroke_c2 = stroke_colors[0], stroke_colors[-1]
    stroke_fill = (
        rnd.randint(min(stroke_c1[0], stroke_c2[0]), max(stroke_c1[0], stroke_c2[0])),
        rnd.randint(min(stroke_c1[1], stroke_c2[1]), max(stroke_c1[1], stroke_c2[1])),
        rnd.randint(min(stroke_c1[2], stroke_c2[2]), max(stroke_c1[2], stroke_c2[2])),
    )
    for i, p in enumerate(text):
        txt_img_draw.text(
            (sum(list_widths[0:i]) + i * char_space_scale * int(not word_split), 0),
            p,
            fill=fill,
            font=image_font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
    return txt_img

def random_color():
    red = random.randrange(256)
    green = random.randrange(256)
    blue = random.randrange(256)
    return '#{0:02X}{1:02X}{2:02X}'.format(red, green, blue)

import math
def random_distorsion(image, vertical, horizontal) -> Tuple:
    if not vertical and not horizontal:
        return image
    max_wave = int(image.height**0.8*rnd.random())
    rand_offset = rnd.randint(0, 180)
    rand_sin_cos = rnd.random()

    func = lambda x: int(
        (math.cos(math.radians(x+rand_offset))*(1-rand_sin_cos) 
        + math.sin(math.radians(x+rand_offset))*rand_sin_cos) * max_wave)
    
    rgb_image = image.convert("RGBA")
    img_arr = np.array(rgb_image)
    vertical_offsets = [func(i) for i in range(img_arr.shape[1])]
    horizontal_offsets = [func(i) for i in range(img_arr.shape[0] + ((max(vertical_offsets) - min(min(vertical_offsets), 0)) if vertical else 0))]
    new_img_arr = np.zeros(
        (img_arr.shape[0] + (2 * max_wave if vertical else 0),
        img_arr.shape[1] + (2 * max_wave if horizontal else 0), 4,)
    )
    new_img_arr_copy = np.copy(new_img_arr)

    if vertical:
        column_height = img_arr.shape[0]
        for i, o in enumerate(vertical_offsets):
            column_pos = (i + max_wave) if horizontal else i
            new_img_arr[max_wave + o : column_height + max_wave + o, column_pos, :] = img_arr[:, i, :]
    if horizontal:
        row_width = img_arr.shape[1]
        for i, o in enumerate(horizontal_offsets):
            if vertical:
                new_img_arr_copy[i, max_wave + o : row_width + max_wave + o, :] = new_img_arr[i, max_wave : row_width + max_wave, :]
            else:
                new_img_arr[i, max_wave + o : row_width + max_wave + o, :] = img_arr[i, :, :]
    return Image.fromarray(np.uint8(new_img_arr_copy if horizontal and vertical else new_img_arr)).convert("RGBA")


def render_data(rand_bg_generator,
    rand_text_generator, rand_font_generator, font_size, word_space_scale, char_space_scale, max_stroke_width,
    random_angle, margin, max_blur_radius, orientation = 0):

    stroke_width = int(max_stroke_width*rnd.random()) if rnd.randint(0,1) else 0
    char_space_scale = int(char_space_scale*rnd.random()) + 0.2 if rnd.randint(0,1) else 1.
    word_space_scale = word_space_scale ** (rnd.random()*2-1) + 0.5
    font_size = font_size + rnd.randint(-4, 4)
    text_color = random_color()
    stroke_fill = text_color if rnd.randint(0,1) else random_color()
    text = rand_text_generator.get_string()
    m_left = random.randrange(0, margin)
    m_top = random.randrange(0, margin)
    m_right = random.randrange(0, margin)
    m_bottom = random.randrange(0, margin)
    font_path = rand_font_generator.get_font_path()
    # render text
    image = _generate_horizontal_text(
        text, font_path, text_color, font_size, 
        word_space_scale, char_space_scale, stroke_width, stroke_fill)

    # Apply distorsion to image #
    image = random_distorsion(image, vertical=True, horizontal=False)

    # rotate image
    if random_angle != 0:
        random_angle = rnd.randint(- random_angle, random_angle)
        image = image.rotate(random_angle, expand=1)
    # Margin #
    image = ImageOps.expand(image, border=(m_left, m_top, m_right, m_bottom))

    background_width, background_height = image.size

    # Background image
    background_img = rand_bg_generator.getImage(background_width, background_height)
    background_img = v2.functional.to_pil_image(background_img)

    # Paste text to background
    background_img.paste(image, (0, 0), image)
    background_img = background_img.convert("RGB")

    # Gaussian blur #
    if max_blur_radius:
        gaussian_filter = ImageFilter.GaussianBlur(rnd.random() * max_blur_radius)
        background_img = background_img.filter(gaussian_filter)

    return background_img, text



# from text_generator.randomTextGenerator import RandomCharGenerator, RandomWordGenerator, RandomSentenceWikiGenerator
# from text_generator.randomFontGenerator import RandomFontGenerator
# from tqdm.auto import tqdm

# if __name__ == '__main__':
#     font_dir = '/Users/apple/OCRDataGenerator/text_generator/fonts'
#     rand_bg_generator = RandomBackground()
#     rand_font_generator = RandomFontGenerator(font_dir)
#     # rand_text_generator = RandomCharGenerator()
#     # rand_text_generator = RandomWordGenerator()
#     rand_text_generator = RandomSentenceWikiGenerator()
#     font_size = 20
#     word_space_scale = 3.0
#     char_space_scale = 3.0
#     stroke_width = 3
#     random_angle = 30
#     blur_radius = 0
#     margin = 40
#     orientation = 0

#     dir_path = "/Users/apple/OCRDataGenerator/vie_dataset"
#     font_path = '/Users/apple/Downloads/Baloo_Bhaijaan_2/BalooBhaijaan2-VariableFont_wght.ttf'
#     label_path = "labels.txt"

#     label_file = open(os.path.join(dir_path, label_path), "w", encoding="utf-8")
#     num_sample = 50000
#     for i in tqdm(range(num_sample)):

#         image, text = render_data(rand_bg_generator,rand_text_generator, rand_font_generator, 
#             font_size, word_space_scale, char_space_scale, stroke_width,
#             random_angle, margin, blur_radius, orientation)
#         # Save the image
#         image_name = "{}.png".format(i)
#         image.save(os.path.join(dir_path, image_name))
#         label_file.write(text + "\n")
#         pass

#     pass



import os
from tqdm import tqdm
from PIL import Image
import pandas as pd
from text_generator.randomTextGenerator import RandomCharGenerator, RandomWordGenerator, RandomSentenceWikiGenerator
from text_generator.randomFontGenerator import RandomFontGenerator
from tqdm.auto import tqdm

def generate_and_save_images(num_samples, dir_path, label_path, font_path, label_file):
    font_size = 20
    word_space_scale = 3.0
    char_space_scale = 3.0
    stroke_width = 3
    random_angle = 30
    blur_radius = 1
    margin = 40
    orientation = 0

    rand_bg_generator = RandomBackground()
    rand_font_generator = RandomFontGenerator(font_dir)
    rand_text_generator = RandomSentenceWikiGenerator()

    df_data = []  # List to store data for DataFrame

    for i in tqdm(range(num_samples)):
        image, text = render_data(rand_bg_generator, rand_text_generator, rand_font_generator, font_size, word_space_scale, char_space_scale, stroke_width, random_angle, margin, blur_radius, orientation)
        image_name = "{}.png".format(i)
        image.save(os.path.join(dir_path, image_name))
        df_data.append([image_name, text])

    # Write data to labels.txt
    with open(os.path.join(dir_path, label_path), "w", encoding="utf-8") as label_file:
        for data in df_data:
            label_file.write(f"{data[0]}\t{data[1]}\n")

if __name__ == '__main__':
    font_dir = '/Users/apple/OCRDataGenerator/text_generator/fonts'
    dir_path = "/Users/apple/OCRDataGenerator/vie_dataset"
    font_path = '/Users/apple/Downloads/Baloo_Bhaijaan_2/BalooBhaijaan2-VariableFont_wght.ttf'
    label_path = "labels.txt"

    label_file = open(os.path.join(dir_path, label_path), "w", encoding="utf-8")
    num_sample = 300000

    generate_and_save_images(num_sample, dir_path, label_path, font_path, label_file)

    # # Create a DataFrame from the labels.txt file using pd.read_fwf and rename the columns
    # df = pd.read_fwf(os.path.join(dir_path, label_path), header=None)
    # df.rename(columns={0: "file_name", 1: "text"}, inplace=True)
