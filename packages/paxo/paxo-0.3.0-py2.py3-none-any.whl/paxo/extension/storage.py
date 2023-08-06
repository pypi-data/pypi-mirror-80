#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import json
import zlib
from collections import OrderedDict


class AbstractStorage(object):
    def __init__(self, path):
        self.data = {}
        self.path = path

    def init(self):
        self.bootstrap()

    def bootstrap(self):
        if not os.path.exists(self.path):
            open(self.path, 'w').write(zlib.compress(json.dumps(self.data)))
        else:
            with open(self.path, 'r') as store:
                path = json.loads(
                    zlib.decompress(store.read()),
                    object_pairs_hook=OrderedDict).get("__PATH__")
                if path:
                    self.path = path
                    open(self.path,
                         'w').write(zlib.compress(json.dumps(self.data)))

    def read(self):
        with open(self.path, 'r') as store:
            self.data = json.loads(zlib.decompress(store.read()),
                                   object_pairs_hook=OrderedDict)

    def save(self):
        with open(self.path, 'w') as store:
            store.write(zlib.compress(json.dumps(self.data)))
