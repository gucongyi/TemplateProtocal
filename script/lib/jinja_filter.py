# coding=utf-8

from jinja2 import environment


def first_upper(source):
    return source[0].upper() + source[1:]


def first_lower(source):
    return source[0].lower() + source[1:]


environment.DEFAULT_FILTERS['first_upper'] = first_upper
environment.DEFAULT_FILTERS['first_lower'] = first_lower
