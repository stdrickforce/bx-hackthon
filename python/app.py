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


from PIL import Image


def session(name):
    sess = tf.Session()
    saver = tf.train.import_meta_graph("./models/%s/export.meta" % name)
    saver.restore(sess, "./models/%s/export" % name)
    return sess


class Handler(object):

    def __init__(self):
        self._r200 = session('r200')
        self._t500 = session('t500')

    def ping(self):
        print("pong")

    def restore_mosaic(self, data):
        return self.restore(data, 'mosaic')

    def restore_bw(self, data):
        return self.restore(data, 'bw')

    def restore(self, data, t='mosaic'):
        input_instance = dict(
            input=base64.urlsafe_b64encode(data).decode("ascii"), key="0"
        )
        input_instance = json.loads(json.dumps(input_instance))

        input_vars = json.loads(tf.get_collection("inputs")[0])
        output_vars = json.loads(tf.get_collection("outputs")[0])
        input = tf.get_default_graph().get_tensor_by_name(input_vars["input"])
        output = tf.get_default_graph().get_tensor_by_name(
            output_vars["output"]
        )

        input_value = np.array(input_instance["input"])

        sess = self._t500 if t == 'mosaic' else self._r200

        output_value = sess.run(
            output, feed_dict={
                input: np.expand_dims(input_value, axis=0)
            }
        )[0]

        output_instance = dict(output=output_value.decode("ascii"), key="0")

        b64data = output_instance["output"]
        b64data += "=" * (-len(b64data) % 4)
        output_data = base64.urlsafe_b64decode(b64data.encode("ascii"))
        return output_data


def image2str(image):
    s = StringIO.StringIO()
    image.save(s, format="png")
    return s.getvalue()


def str2image(data):
    s = StringIO.StringIO(data)
    return Image.open(s)

hackthon_thrift = thriftpy.load("../hackthon.thrift")
