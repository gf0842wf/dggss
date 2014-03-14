# -*- coding: utf-8 -*-

class dotdict(dict):
    '''用于操作 dict 对象

    >>> dd = dotdict(a=1, b=2)
    >>> dd.c = 3
    >>> dd
    {'a': 1, 'c': 3, 'b': 2}
    >>> del dd.c
    >>> dd
    {'a': 1, 'b': 2}
    '''
    def __getitem__(self, name):
        value = dict.__getitem__(self, name)
        if isinstance(value, dict) and not isinstance(value, dotdict):
            value = dotdict(value)
        return value

    __getattr__ = __getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class dotdictex(dotdict):
    '''dotdict 的扩展，支持多级直接赋值

    >>> ddx = dotdictex()
    >>> ddx[1][1] = 1
    >>> ddx.a.a = 'a'
    >>> ddx
    {'a': {'a': 'a'}, 1: {1: 1}}
    '''
    def __getitem__(self, name):
        if name not in self:
            return self.setdefault(name, dotdictex())
        return dotdict.__getitem__(self, name)

    __getattr__ = __getitem__
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    
__all__ = ["dotdict", "dotdictex"]