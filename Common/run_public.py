# -*- coding: utf-8 -*-

import importlib


def exe_module(module, method, args):
    cls = module.split(".")[-1]
    # print cls
    if len(module.split(".")) > 2:
        module = module[0:-(len(module.split(".")[-1])+1)]
    else:
        module = module
    m = importlib.import_module(module,)
    mod = getattr(m, cls)
    obj = mod()
    function = getattr(obj, method)
    va = apply(function, args)
    return va


class Context(object):
    """
    Define the Context to store the return value.
    """
    def __init__(self):
        self.key_value = {}


if __name__ == "__main__":
    context = Context()
    exe_module("PublicModule.RunPublic", "backendLogin", (context,))
    exe_module("PublicModule.RunPublic", "getStoreIdFromList", (context, 8))
