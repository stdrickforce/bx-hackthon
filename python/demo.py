#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com> <fantengyuan@baixing.com>

import os

from PIL import (Image)

from thriftpy.rpc import make_client

from app import (
    image2str,
    str2image,
    hackthon_thrift,
)

from generate_train_data import (  # noqa
    mosaic,
    bw,
)

client = make_client(hackthon_thrift.Hackthon, "127.0.0.1", 9099)


def squarize(image, size=256, offset=0):
    width, height = image.size
    if width < height:
        width, height = size, int(height * (float(size) / float(width)))
        x1, y1 = 0, height / 2 - 128 - offset
    else:
        height, width = size, int(width * (float(size) / float(height)))
        y1, x1 = 0, width / 2 - 128 - offset
    image = image.resize((width, height))
    return image.crop((x1, y1, x1 + size, y1 + size))


def process_bw(filename, offset=0):
    image = Image.open(filename)
    image = squarize(image, 256, offset)
    image1 = bw(image)
    image2 = str2image(client.restore_bw(image2str(image1)))
    return image1, image2


def process_mosaic(filename, show=False, offset=0):
    image = Image.open(filename)
    image = squarize(image, 256, offset)
    image1 = mosaic(image, 4)

    s = image2str(image1)
    s = client.restore_mosaic(s)
    image2 = str2image(s)
    return image1, image2


def concrete(directory, name):
    filenames = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.startswith("."):
                continue
            filename = os.path.join(root, f)
            filenames.append(filename)

    image = Image.new('RGB', (256 * 3, 256 * len(filenames)), (255, 255, 255))
    for i, filename in enumerate(filenames):
        print(i)
        img0 = Image.open(filename)
        img0 = squarize(img0, 256)

        img1, img2 = process_mosaic(filename)
        image.paste(img0, (0, 256 * i))
        image.paste(img1, (256, 256 * i))
        image.paste(img2, (512, 256 * i))
    image.save("%s.png" % name)


def merge(img1, img2):
    image = Image.new('RGB', (512, 256), (255, 255, 255))
    image.paste(img1, (0, 0))
    image.paste(img2, (256, 0))
    image.show()


if __name__ == '__main__':
    concrete("./series/mingxing", "mingxing-a")
    # img1, img2 = process_bw(
    #     "/Users/stdrickforce/Downloads/WechatIMG287.jpeg",
    #     offset=0
    # )
    # merge(img1, img2)
    # process("./sumiao/yaogun.jpg")
    # process('./bw/1401.png')
    # process('./series/history/3.pic.jpg')
    # process('/Users/stdrickforce/Downloads/heshen.jpg')
    # process('/Users/stdrickforce/Downloads/75b58PICKcC_1024.jpg')
    # process('/Users/stdrickforce/Downloads/xiangfei.jpg')
    # process('/Users/stdrickforce/Pictures/mayun.jpeg')
    client.close()
