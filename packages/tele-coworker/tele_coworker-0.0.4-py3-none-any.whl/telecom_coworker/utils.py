from collections import defaultdict
from threading import Timer


def set_interval(func, interval=5):
    def wrap_func():
        func()
        Timer(interval, wrap_func).start()

    Timer(interval, wrap_func).start()


def search_dict_by_keys(source: dict, values):
    result = defaultdict(set)
    for k, vs in source.items():
        for v in vs:
            if v in values:
                result[k].add(v)
    return result


if __name__ == '__main__':
    d = defaultdict(set)
    d['foo'].add('bar')
    d['foo'].add('bar2')
    d['bar'] = set()

    result = search_dict_by_keys(d, ['bar'])
    print(result)
