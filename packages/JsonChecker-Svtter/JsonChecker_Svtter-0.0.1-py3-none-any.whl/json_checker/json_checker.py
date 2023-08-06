import json
from typing import Tuple


def key_checker(dict1: dict, dict2: dict) -> Tuple[bool, str]:
    for k in set(dict1) | set(dict2):
        if k not in dict1:
            return False, f'dict1 do not have key: {k}'
        if k not in dict2:
            return False, f'dict2 do not have key: {k}'

    return True, 'Key is fine.'


def structure(dict1 :dict, dict2: dict) -> Tuple[bool, str]:

    is_equal, msg = key_checker(dict1, dict2)
    if not is_equal:
        return False, msg

    for k, v in dict1.items():
        v2 = dict2[k]
        if type(v) != type(v2):
            return False, f"error on value: dict1.{k} is {type(v)}, dict2.{k} is {type(v2)}"
        elif type(v) == dict:
            is_equal, msg = structure(v, v2)
            if not is_equal:
                return is_equal, msg
    return True, 'Everything is fine.'


def check_from_file(file_path, dictionary: dict) -> Tuple[bool, str]:
    with open(file_path, 'r') as f:
        dict1 = json.load(file_path)
        return structure(dict1, dictionary)
