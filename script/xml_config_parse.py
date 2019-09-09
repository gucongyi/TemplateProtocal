# coding=utf-8

import sys

from lib import variable_util
from lib import xml_util

_pojo_map = {}
_pojo_package = None


# 收集msg和response
def collect_pojo_from_files():
    if _pojo_package is not None:
        return _pojo_map

    data = xml_util.read_config('../config/ProtoServerClass.xml')

    pojos_config = None
    # 标签列表
    label_list = ['req', 'class', 'enum', 'resp']
    if 'msgs' in data:
        pojos_config = data['msgs']

    if pojos_config is not None:
        # 解析标签
        for label in label_list:
            if label in pojos_config:
                pojo_config_list = []
                _pojo_map[label] = {}
                pojos = pojos_config[label]
                if isinstance(pojos, dict):
                    pojo = {'package': pojos_config['package']}
                    pojo_config_list.append(pojo)
                    for (k, v) in pojos.items():
                        pojo[k] = v
                else:
                    for pojo in pojos:
                        pojo['package'] = pojos_config['package']
                        pojo_config_list.append(pojo)
                for pojo_config in pojo_config_list:
                    pojo = parse_bean(pojo_config)
                    pojo['serializeByte'] = True
                    _pojo_map[label][pojo['name']] = pojo
                    check_pojo(pojo, [], 1)  
    return _pojo_map


def parse_bean(config):
    bean = {
        'name': config['name'],
        'properties': []
    }
    # 属性列表
    attr_list = ['extends', 'des', 'resp', 'type']
    for attr in attr_list:
        if attr in config:
            bean.setdefault(attr, config[attr])
    parse_properties_from_xml_config(config, bean)
    return bean


def check_pojo(bean, can_not_named_property, start_index):
    had_indexs = []
    had_names = []
    for property in bean['properties']:
        if property['name'] in can_not_named_property:
            raise Exception('%s property:%s can not named %s!' % (bean['name'], property['name'], property['name']))
        if property['name'] in had_names:
            raise Exception('%s name:%s 名字重复!' % (bean['name'], property['name']))
        had_names.append(property['name'])


# 解析属性
def parse_properties_from_xml_config(config, result_bean):
    if 'field' in config:
        if isinstance(config['field'], dict):
            property = {
                'type': variable_util.remove_type_with_java_lang_package(
                    config['field']['type'].replace('[', '<').replace(']', '>')),
                'name': config['field']['name'],
                'des': config['field']['des'],
            }
            result_bean['properties'].append(property)
        else:
            for property_arr in config['field']:
                property = {
                    'name': property_arr['name'],
                }
                # 如果xml中field多了一些属性，这里也要加上
                if 'value' in property_arr:
                    property.setdefault('value', property_arr['value'])
                if 'des' in property_arr:
                    property.setdefault('des', property_arr['des'])
                if 'type' in property_arr:
                    property.setdefault('type', property_arr['type'].replace('[', '<').replace(']', '>'))
                result_bean['properties'].append(property)