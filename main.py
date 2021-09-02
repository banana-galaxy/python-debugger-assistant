import importlib

def load(file_name):
    try:
        module = importlib.import_module(file_name.split('.')[0])
        return f"module loaded", module, [i for i in dir(module) if '__' not in i]
    except BaseException as e:
        return f"failed to load module: {e}", 0

def reload(module):
    try:
        importlib.reload(module)
        return "module reloaded", [i for i in dir(module) if '__' not in i]
    except BaseException as e:
        return f"failed to reload module: {e}", 0

def exit():
    pass
    # this may or may not need code depending on how the tui will work

if '__main__' == __name__:
    print(load('tes'))