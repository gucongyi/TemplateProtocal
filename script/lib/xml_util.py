# coding=utf-8

import xmltodict


# 读取配置文件
def read_config(filename):
    with open(filename, 'rb') as entity_config_file:
        config_str = entity_config_file.read()
    config = xmltodict.parse(config_str)
    # return _parse_config(config)
    return _parse_xml_object(config)


# # 去掉属性中的@
# def _parse_config(original_object):
#     expect_map = {}
#     for (k, v) in original_object.items():
#         parsed_key = k
#         if str(k).startswith('@'):
#             parsed_key = k[1:]
#
#         if isinstance(v, dict):
#             expect_map[parsed_key] = _parse_config(v)
#         else:
#             expect_map[parsed_key] = v
#
#     return expect_map


# 转换xml解析出来k中的@
def _parse_xml_object(ob):
    if isinstance(ob, dict):
        remove = []
        add = {}
        for (k, v) in ob.items():
            _parse_xml_object(v)
            if k.startswith('@'):
                remove.append(k)
                add[k[1:]] = v

        for item in remove:
            ob.pop(item)
        for (k, v) in add.items():
            ob[k] = v
    elif isinstance(ob, list):
        for v in ob:
            _parse_xml_object(v)

    return ob
