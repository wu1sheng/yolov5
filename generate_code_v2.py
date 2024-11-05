#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Use `pip install captcha` and `pip install pillow` to install dependencies
###
import os
import shutil
import random
from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
from tqdm import tqdm

NUMBER = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']

ALL_CHAR_SET = NUMBER + alphabet + ALPHABET

# 最终生成的验证码数量
count = 10

# 参数: 宽度、高度、字符长度、字体大小
img_width, img_height, labelno, fontsize = 200, 100, 4, [42, 50, 56]


def generate_random_color():
    c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return c


def generate_random_location(lx, ly, rx, ry):
    return random.randint(lx, rx), random.randint(ly, ry)


def draw_code_v2():
    w, h, code_len, font_size = 125, 45, 4, [30, 35, 40]
    # background = np.ones((w, h, 3), dtype=np.uint8) * np.array([254, 230, 224])
    background = Image.new('RGB', (w, h), (224, 230, 254))
    line_color = generate_random_color()
    draw = ImageDraw.Draw(background)
    for i in range(random.randint(2, 6)):
        draw.line((generate_random_location(0, 0, w, h), generate_random_location(0, 0, w, h)), width=1,
                  fill=line_color)
    s = ''
    txt = ''
    for i in range(code_len):
        fontpath = r"C:\Windows\Fonts\simhei.ttf"
        ch_font_size = random.choice(font_size)
        font = ImageFont.truetype(fontpath, ch_font_size)
        # 绘制文字信息
        select_char_idx = random.randint(0, len(ALL_CHAR_SET) - 1)
        s += ALL_CHAR_SET[select_char_idx]
        text_x, text_y = generate_random_location(int(i / 4 * w), 0, int((i + 1) / 4 * w - ch_font_size / 2),
                                                  int(h / 8))
        draw.text((text_x, text_y), s[-1], font=font, fill=generate_random_color())
        x1, y1, x2, y2 = draw.textbbox((text_x, text_y), s[-1], font=font)
        line = f'{select_char_idx} {(x1 + x2) / 2 / w} {(y1 + y2) / 2 / h} {(x2 - x1) / w} {(y2 - y1) / h}\n'
        txt += line
        # draw.text((0, 0),
        #           random.choice(ALL_CHAR_SET), font=font, fill=generate_random_color())
    if not os.path.exists('confirm_code'):
        os.makedirs('confirm_code')
    if not os.path.exists('confirm_code_label'):
        os.makedirs('confirm_code_label')
    background.save(f'confirm_code/{s}.png')
    with open(f'confirm_code_label/{s}.txt', 'w') as f:
        f.write(txt)
        f.close()


def divide_dir(img_src=r"confirm_code",
               label_src=r"confirm_code_label"):
    img_dst = "datasets\code\images"
    label_dst = "datasets\code\labels"
    imgs = os.listdir(img_src)
    random.shuffle(imgs)
    train = imgs[:int(0.7 * len(imgs))]
    val = imgs[int(0.7 * len(imgs)):int(0.9 * len(imgs))]
    test = imgs[int(0.9 * len(imgs)):]
    for img in train:
        shutil.copy(os.path.join(img_src, img), os.path.join(img_dst, 'train', img))

        shutil.copy(os.path.join(label_src, img.replace('.png', '.txt')),
                    os.path.join(label_dst, 'train', img.replace('.png', '.txt')))
    for img in val:
        shutil.copy(os.path.join(img_src, img), os.path.join(img_dst, 'val', img))

        shutil.copy(os.path.join(label_src, img.replace('.png', '.txt')),
                    os.path.join(label_dst, 'val', img.replace('.png', '.txt')))
    for img in test:
        shutil.copy(os.path.join(img_src, img), os.path.join(img_dst, 'test', img))

        shutil.copy(os.path.join(label_src, img.replace('.png', '.txt')),
                    os.path.join(label_dst, 'test', img.replace('.png', '.txt')))


if __name__ == '__main__':
    # for i in tqdm(range(8)):
    #     draw_code_v2()
    divide_dir()
    # ALL_CHAR_dic = dict()
    # for i in range(len(ALL_CHAR_SET)):
    #     ALL_CHAR_dic[i]=ALL_CHAR_SET[i]
    # pass
