import sys
from inspect import getmembers, isfunction
from typing import Callable

import validators


def validate(msg, current_func, FUNC_MAPPER):
    print(f"[{current_func}] validate data: {msg.text}")
    func_validators = FUNC_MAPPER[current_func].get("validators", [])
    err = None
    FUNC_MAPPER[current_func]["err_msg"] = err

    for validator in func_validators:
        func = search_func_in_module(validator, "validators")
        if func:
            err = func(msg.text)
        else:
            print(f"[{func_validators}] no such functions in module 'validators'")
        if err:
            FUNC_MAPPER[current_func]["err_msg"] = err
            break


def search_func_in_module(func: str, module: str) -> Callable:
    module = sys.modules[module]
    module_funcs = getmembers(module, isfunction)
    module_funcs = dict(module_funcs)
    func_object = module_funcs.get(func)
    return func_object


# TODO Write validator for persons amount -> must be 1 to 4 persons
# TODO City Validator + City hints (list all Cities)
# TODO Hotel Validator + Hotel hints (list all Hotels for City)
