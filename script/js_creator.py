# coding=utf-8

import sys
import tkinter as tk
from tkinter import filedialog
import codecs
import xml_config_parse

from jinja2 import Environment, FileSystemLoader
from lib import file_util, jinja_filter

environment = Environment(loader=FileSystemLoader(searchpath='./template'))

def create_server():
    root = tk.Tk()
    root.withdraw()

    # 从文件中获取路径
    f = codecs.open('../config/outpath_js.txt', 'r', 'utf-8', buffering=True)
    outpath = f.read()
    f.close()
    outpath = outpath.strip("/") + '/'
    # 手动选择文件夹
    # outpath = filedialog.askdirectory() 
    # outpath += '/'

    pojo_map = xml_config_parse.collect_pojo_from_files()
    file_util.mkdir(outpath)


    class_dict = {}
    req_dict = {}
    enum_dict = {}
    for (k, v) in pojo_map.items():
        if k is 'req':
            for key, value in v.items():
                class_dict.setdefault(key, value)
                req_dict.setdefault(key, value)
        if k is 'resp':
            for key, value in v.items():
                req_dict.setdefault(key, value)
                class_dict.setdefault(key, value)
        if k is 'enum':
            for key, value in v.items():
                enum_dict.setdefault(key, value)
        if k is 'class':
            for key, value in v.items():
                if 'type' in value and value['type'] == 'CodeError':
                    req_dict.setdefault(key, value)
                else:
                    class_dict.setdefault(key, value)
        
    if class_dict:
        class_dict_plus = {}
        class_dict_plus['datas'] = class_dict
        # 选择模板
        template_bean_server = environment.get_template('js.temp')
        with open(outpath + 'ProtoServerClass.js', 'w', encoding='utf-8') as out_file:
            pojo_server_file = template_bean_server.render(class_dict_plus)
            out_file.write(pojo_server_file)
            print('create pojo ProtoServerClass.js success')
    if req_dict:
        req_dict_plus = {}
        req_dict_plus['datas'] = req_dict
        template_bean_server = environment.get_template('js_code.temp')
        with open(outpath + 'ProtoServerCode.js', 'w', encoding='utf-8') as out_file:
            pojo_server_file = template_bean_server.render(req_dict_plus)
            out_file.write(pojo_server_file)
            print('create pojo ProtoServerCode.js success')
    if enum_dict:
        enum_dict_plus = {}
        enum_dict_plus['datas'] = enum_dict
        template_bean_server = environment.get_template('js_enum.temp')
        with open(outpath + 'ProtoServerEnum.js', 'w', encoding='utf-8') as out_file:
            pojo_server_file = template_bean_server.render(enum_dict_plus)
            out_file.write(pojo_server_file)
            print('create pojo ProtoServerEnum.js success')

if __name__ == '__main__':
    try:
        create_server()
    except:
        print('create pojo error!')
        raise