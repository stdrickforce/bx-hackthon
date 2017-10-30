#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com> <fantengyuan@baixing.com>

import os

from PIL import Image, ImageDraw  # noqa

from app import (
    Handler,
    image2str,
    str2image,
)

WIDTH = 256
HEIGHT = 256
GRANULARITY = 4


def mosaic(f, granularity):
    image = Image.new('RGB', f.size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    for x in range(0, image.size[0], granularity):
        for y in range(0, image.size[1], granularity):
            r, g, b = f.getpixel((x, y))
            x1, y1 = x, y
            x2, y2 = x + granularity, y + granularity
            draw.rectangle(
                [(x1, y1), (x2, y2)], fill=(r, g, b), outline=None
            )  # None即是不加网格
    return image


def bw(f):
    return f.convert('L')


def do(filename, count):
    f = Image.open(filename)
    f = f.resize((WIDTH, HEIGHT))

    def do_resize():
        f.save("source/%04d.png" % count, 'png')

    def do_mosaic():
        image = mosaic(f, 4)
        image.save("mosaic/%04d.png" % count, 'png')

    def do_bw():
        image = f.convert('L')
        image.save("bw/%04d.png" % count, 'png')

    do_resize()
    do_bw()


def iterfolder():
    count = 1
    for root, dirs, files in os.walk("./lfw"):
        for f in files:
            if not f.endswith(".jpg"):
                continue
            filename = os.path.join(root, f)
            print("%d: %s" % (count, filename))
            do(filename, count)
            count += 1
            break


def iterfolder2():

    h = Handler()
    for root, dirs, files in os.walk("./mosaic"):
        for f in files:
            filename = os.path.join(root, f)
            print(filename)
            image = Image.open(filename)
            s = h.restore(image2str(image))
            image = str2image(s)
            image.save("./restore/%s" % f)


if __name__ == '__main__':
    iterfolder()
    # filename = "04-012440_543.jpg"
    # newfilename = "./train/1.jpg"
    # mosaic(filename, newfilename)
