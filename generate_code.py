#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Use `pip install captcha` and `pip install pillow` to install dependencies
###

import cv2
from tkinter import font

import numpy as np
from captcha.image import ImageCaptcha
from PIL import Image
import random
import time
import os, sys, ast

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


def generate_random_location(w, h):
    return random.randint(-int(0.2 * w), int(1.2 * w)), random.randint(-int(0.2 * h), int(1.2 * h))


def draw_code():
    w, h, code_len, font_size = 300, 800, 4, [5, 10, 15]
    code_str = 'Ab1T'
    background = np.ones((w, h, 3), dtype=np.uint8)*255
    for i in range(random.randint(2, 8)):
        cv2.line(background, generate_random_location(w, h), generate_random_location(w, h), generate_random_color())
    for s in code_str:
        cv2.putText(background, s, generate_random_location(w, h),
                    cv2.FONT_HERSHEY_COMPLEX, random.choice(font_size), generate_random_color(), 5)
    cv2.imshow('sss', background)
    cv2.waitKey()


def mylist(x):
    if isinstance(x, (list, tuple)):
        return x
    else:
        return [x]


def get_argv():
    global img_width, img_height, labelno, fontsize, count
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            arg = sys.argv[i].split('=')
            if arg[0] == 'w':
                img_width = int(arg[1])
            if arg[0] == 'h':
                img_height = int(arg[1])
            if arg[0] == 'n':
                labelno = int(arg[1])
            if arg[0] == 'c':
                count = int(arg[1]) + 1
            if arg[0] == 'fontsize':
                # fontsize = mylist(int(arg[1]))
                fontsize = ast.literal_eval(arg[1])
    print(f'img_width:{img_width}, img_height:{img_height}, labelno:{labelno},fonsize:{fontsize},filecount={count}')


def random_captcha_text():
    global labelno
    captcha_text = []
    for i in range(labelno):
        c = random.choice(ALL_CHAR_SET)
        captcha_text.append(c)
    return ''.join(captcha_text)


# 生成字符对应的验证码
def gen_captcha_text_and_image():
    global img_width, img_height, fontsize
    image = ImageCaptcha(width=img_width, height=img_height, fonts=[r'C:\Windows\Fonts\simsun.ttc'],
                         font_sizes=fontsize)
    captcha_text = random_captcha_text()
    # print('captcha_text:',captcha_text)
    captcha_image = Image.open(image.generate(captcha_text))
    return captcha_text, captcha_image


def main():
    global img_width, img_height, count, labelno
    get_argv()
    # 保存路径
    path = f'{img_width}x{img_height}_{labelno}chars'
    print('save path:', path)
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(count):
        now = str(int(time.time()))
        text, image = gen_captcha_text_and_image()
        filename = text + '_' + now + '.png'
        image.save(path + os.path.sep + filename)
        print('saved %d : %s' % (i + 1, filename))


if __name__ == '__main__':
    draw_code()
    # main()
