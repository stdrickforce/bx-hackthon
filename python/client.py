#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com> <fantengyuan@baixing.com>

from PIL import Image

from app import (
    image2str,
    str2image,
    hackthon_thrift,
)

from thriftpy.rpc import make_client

client = make_client(hackthon_thrift.Hackthon, "127.0.0.1", 9099)
image = Image.open("./mosaic/1001.png")

s = client.restore(image2str(image))
str2image(s).show()

s = client.restore(s)
str2image(s).show()

client.close()

if __name__ == "__main__":
    pass
