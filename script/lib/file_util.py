# coding=utf-8
import os
import shutil


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    is_exist = os.path.exists(path)
    if not is_exist:
        os.makedirs(path)


def rmdir(path):
    is_exist = os.path.exists(path)
    if is_exist:
        shutil.rmtree(path)


def read_file(filename):
    with open(filename) as file:
        return file.read()