def Read_File():
    with open("debug.txt") as f:
        return __import__("pprint").pformat(eval(f.read()))


def hi():
    return {"hello": 123, "dorime": ["item1", "item2", "cheemsadidas", {"hello!": 1}]}


class Hey:
    pass


def my_func():
    return Hey()
