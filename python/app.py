#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com> <fantengyuan@baixing.com>

import json
import base64
import tensorflow as tf
import numpy as np
import StringIO
import thriftpy

from thriftpy.thrift import TProcessor

from PIL import Image

MODEL = './models/t10'


def image2str(image):
    s = StringIO.StringIO()
    image.save(s, format="png")
    return s.getvalue()


def str2image(data):
    s = StringIO.StringIO(data)
    return Image.open(s)


def read(filename):
    f = Image.open(filename)
    f = f.resize((256, 256))
    return image2str(f)


def resize(data):
    img = str2image(data)
    img = img.resize((256, 256))
    return image2str(img)


def restore(data):
    data = resize(data)

    input_instance = dict(
        input=base64.urlsafe_b64encode(data).decode("ascii"),
        key="0"
    )
    input_instance = json.loads(json.dumps(input_instance))

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph("%s/export.meta" % MODEL)
        saver.restore(sess, "%s/export" % MODEL)
        input_vars = json.loads(tf.get_collection("inputs")[0])
        output_vars = json.loads(tf.get_collection("outputs")[0])
        input = tf.get_default_graph().get_tensor_by_name(input_vars["input"])
        output = tf.get_default_graph().get_tensor_by_name(
            output_vars["output"]
        )

        input_value = np.array(input_instance["input"])
        output_value = sess.run(
            output,
            feed_dict={input: np.expand_dims(input_value, axis=0)}
        )[0]

    output_instance = dict(output=output_value.decode("ascii"), key="0")

    b64data = output_instance["output"]
    b64data += "=" * (-len(b64data) % 4)
    output_data = base64.urlsafe_b64decode(b64data.encode("ascii"))
    return output_data


class Handler(object):

    def ping(self):
        print("pong")

    def restore(self, image_bytes):
        return restore(image_bytes)


hackthon_thrift = thriftpy.load("../hackthon.thrift")
app = TProcessor(hackthon_thrift.Hackthon, Handler())


if __name__ == '__main__':
    h = Handler()
    a = read("/Users/stdrickforce/Pictures/cms.png")
    h.restore(a)
