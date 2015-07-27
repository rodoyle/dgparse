#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Centralized Parser for models coming from delimiter separated value files
"""

import csv
import os
import functools


def clean_record(basename, record):
    result = {'type_': basename.split('.')[0]}
    for key, value in record.iteritems():
        if key is '':
            msg = "{0} contains a NonRecord Entry {1}".format(basename, record)
            result['ERROR'] = msg
        if '.' in key:
            parent_attr, child_attr = key.split('.')
            if parent_attr in result:
                result[parent_attr][child_attr] = value
            else:
                result[parent_attr] = {child_attr: value}
        else:
            result[key] = value
    return result


def parse(open_file, fieldnames=None, record_type=None):
    """
    Parse an open file object
    :param open_file:
    :return:
    """
    # What does this file contain?
    if not record_type:
        record_type = os.path.basename(open_file.name)
    record_cleaner = functools.partial(clean_record, record_type)
    return map(record_cleaner, csv.DictReader(open_file, fieldnames))

