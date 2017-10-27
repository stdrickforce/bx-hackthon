#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com> <fantengyuan@baixing.com>

import os

from PIL import Image, ImageDraw  # noqa

WIDTH = 256
HEIGHT = 256
GRANULARITY = 4


def do(filename, count):
    f = Image.open(filename)
    f = f.resize((WIDTH, HEIGHT))

    def resize():
        f.save("source/%04d.png" % count, 'png')

    def mosaic():
        image = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        for x in range(0, WIDTH, GRANULARITY):
            for y in range(0, HEIGHT, GRANULARITY):
                r, g, b = f.getpixel((x, y))
                x1, y1 = x, y
                x2, y2 = x + GRANULARITY, y + GRANULARITY
                draw.rectangle(
                    [(x1, y1), (x2, y2)], fill=(r, g, b), outline=None
                )  # None即是不加网格
        image.save("mosaic/%04d.png" % count, 'png')

    resize()
    mosaic()


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


if __name__ == '__main__':
    iterfolder()
    # filename = "04-012440_543.jpg"
    # newfilename = "./train/1.jpg"
    # mosaic(filename, newfilename)
