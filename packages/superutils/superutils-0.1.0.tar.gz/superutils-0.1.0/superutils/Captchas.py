#!/usr/bin/env python
# coding: utf-8
# author: Frank YCJ
# email: 1320259466@qq.com


from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import time


# 随机字母:
def _rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def _rndColor1():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def _rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def get_captcha(save_path, width=240, height=60, font_path='/Library/Fonts/Arial.ttf', font_size=36):
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    # font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 36)
    font = ImageFont.truetype(font_path, font_size)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=_rndColor1())
    # 输出文字:
    for t in range(4):
        draw.text((60 * t + 10, 10), _rndChar(), font=font, fill=_rndColor2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    file_name = str(time.time()).replace(".", "") + ".jpg"
    file_path = save_path + "/" + file_name
    image.save(file_path, 'jpeg');
    return file_name



