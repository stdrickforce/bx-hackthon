#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: stdrickforce (Tengyuan Fan)
# Email: <stdrickforce@gmail.com> <fantengyuan@baixing.com>

from thriftpy.thrift import TProcessor

from app import (
    hackthon_thrift,
    Handler,
)

app = TProcessor(hackthon_thrift.Hackthon, Handler())
