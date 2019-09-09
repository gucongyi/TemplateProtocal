# coding=utf-8


# 是否是entity 属性类型
def is_entity_property_type(property_type):
    return property_type in ['boolean', 'byte', 'short', 'int', 'long', 'float', 'double', 'String']


def map_to_db_type(property_type, db):
    if db == 'mysql':
        types = {
            'boolean': 'boolean',
            'byte': 'tinyint',
            'short': 'smallint',
            'int': 'int',
            'long': 'bigint',
            'float': 'float',
            'double': 'double',
            'string': 'varchar',
        }
        if property_type.lower() in types:
            return types[property_type.lower()]

        return 'json'
    elif db == 'postgresql':
        types = {
            'boolean': 'boolean',
            'byte': 'smallint',
            'short': 'smallint',
            'int': 'int',
            'long': 'bigint',
            'float': 'float',
            'double': 'double precision',
            'string': 'varchar',
        }
        if property_type.lower() in types:
            return types[property_type.lower()]

        return 'json'
    else:
        return None


# 获取类型默认值
def get_type_default_value(var_type):
    types = {
        'boolean': 'false',
        'byte': '0',
        'short': '0',
        'int': '0',
        'long': '0L',
        'float': '0F',
        'double': '0',
        'Boolean': 'false',
        'Byte': '0',
        'Short': '0',
        'Integer': '0',
        'Long': '0L',
        'Float': '0F',
        'Double': '0',
        'String': 'null',
    }
    return types[var_type] if var_type in types else 'null'


def default_to_sql_default(var_type, value):
    if var_type.lower() in ['long', 'float']:
        return value.replace('L', '').replace('l', '').replace('F', '').replace('f', '')

    if value == 'null':
        return None
    return value


# 是否是list类型
def is_list_type(var_type):
    return var_type.find('List<') == 0 or var_type == 'List'


# 是否是map类型
def is_map_type(var_type):
    return var_type.find('Map<') == 0 or var_type == 'Map'


# 是否是set类型
def is_set_type(var_type):
    return var_type.find('Set<') == 0 or var_type == 'Set'


def is_container_type(var_type):
    return is_list_type(var_type) or is_map_type(var_type) or is_set_type(var_type)


def _find_map_split_child_index(type):
    left = 0
    for index in range(0, len(type)):
        if left == 0 and type[index] == ',':
            return index
        if type[index] == '<':
            left = left + 1
        if type[index] == '>':
            left = left - 1


# 获取容器包含的数据类型
def get_inner_types(var_type):
    var_type = var_type.replace(' ', '')
    inner_types = set([])
    if is_container_type(var_type):
        # 含有容器
        start = var_type.find('<')
        stop = var_type.rfind('>')
        container_type = var_type[0:start]

        child_type = var_type[start + 1:stop]
        if container_type == 'Map':
            split_index = _find_map_split_child_index(child_type)
            inner_types = inner_types.union(get_inner_types(child_type[:split_index]))
            inner_types = inner_types.union(get_inner_types(child_type[split_index + 1:]))
        else:
            inner_types = inner_types.union(get_inner_types(child_type))
    else:
        inner_types.add(var_type)

    return inner_types


def _get_type_info(child_type):
    if is_set_type(child_type):
        child_top_type = {'type': 'Set', 'isComplexType': True}
    elif is_list_type(child_type):
        child_top_type = {'type': 'List', 'isComplexType': True}
    elif is_map_type(child_type):
        child_top_type = {'type': 'Map', 'isComplexType': True}
    elif is_complex_type(child_type):
        child_top_type = {'type': child_type, 'isComplexType': True}
    else:
        child_top_type = {'type': child_type, 'isComplexType': False}
    return child_top_type


def get_inner_top_types_info(var_type):
    var_type = var_type.replace(' ', '')

    if is_list_type(var_type) or is_set_type(var_type):
        start = var_type.find('<')
        stop = var_type.rfind('>')
        child_type = var_type[start + 1:stop]
        return [_get_type_info(child_type)]
    if is_map_type(var_type):
        start = var_type.find('<')
        stop = var_type.rfind('>')
        child_type = var_type[start + 1:stop]
        split_index = _find_map_split_child_index(child_type)
        return [_get_type_info(child_type[:split_index]), _get_type_info(child_type[split_index + 1:])]
    return []


# 是否是原始基本类型
def is_original_type(var_type):
    if var_type in ['boolean', 'char', 'byte', 'short', 'int', 'long', 'float', 'double']:
        return True
    return False


# 是否是封装类型
def is_box_type(var_type):
    if var_type in ['Boolean', 'Char', 'Byte', 'Short', 'Integer', 'Long', 'Float', 'Double', 'String',
                    'java.lang.Boolean', 'java.lang.Char', 'java.lang.Byte', 'java.lang.Short', 'java.lang.Integer',
                    'java.lang.Long', 'java.lang.Float', 'java.lang.Double', 'java.lang.String']:
        return True
    return False


# 是否是复杂类型
def is_complex_type(var_type):
    return not (is_original_type(var_type) or is_box_type(var_type))


def remove_type_with_java_lang_package(type):
    return type.replace('java.lang.', '')


not_need_import_types = ['boolean', 'char', 'byte', 'short', 'int', 'long', 'float', 'double',
                         'Boolean', 'Char', 'Byte', 'Short', 'Int', 'Long', 'Float', 'Double',
                         'String', 'Object', '']


def get_type_imports(var_type):
    var_type = var_type.replace(' ', '')
    type_imports = set()
    if is_container_type(var_type):
        # 含有容器
        start = var_type.find('<')
        stop = var_type.rfind('>')
        container_type = var_type[0:start]

        if container_type not in not_need_import_types:
            type_imports.add('import java.util.%s;\n' % container_type)

        child_type = var_type[start + 1:stop]
        if child_type.find('<') > -1:
            child_imports = get_type_imports(child_type)
            type_imports = type_imports.union(child_imports)
            return type_imports

        children_type = child_type.split(',')
        for index in range(len(children_type)):
            child_imports = get_type_imports(children_type[index])
            type_imports = type_imports.union(child_imports)

    return type_imports


# java 类型转ts类型
def type_java_to_ts(var_type):
    number_types = ['byte', 'short', 'int', 'long', 'float', 'double', 'integer']
    if var_type.lower() in number_types:
        return 'number'
    if var_type == 'String':
        return 'string'
    if var_type == 'Map':
        return 'Object'

    return var_type


# sql 类型转ts类型
def type_sql_to_ts(var_type):
    number_types = ['tinyint', 'smallint', 'mediumint', 'integer', 'int', 'bigint', 'float', 'double', 'decimal']
    if var_type.lower() in number_types:
        return 'number'

    string_types = ['char', 'varchar', 'tinyblob', 'tinytext', 'blob', 'text', 'mediumblob', 'mediumtext', 'logngblob',
                    'longtext', 'varbinary', 'binary']
    if var_type in string_types:
        return 'string'

    return var_type
