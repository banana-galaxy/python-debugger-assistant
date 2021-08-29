import sys, importlib, re
file = sys.argv[1].split('.')[0]
module = importlib.import_module(file)
done = False

while not done:
    user = input()
    if user == "exit":
        done = True
    elif user == "reload":
        try:
            importlib.reload(module)
        except BaseException as e:
            print(f"unable to reload module: {e}")
        print()
    else:
        if "(" not in user:
            print("Please call a function the same way you would in python\n")
            continue
        method, args = user.split('(')
        args = re.findall("\w+", args)
        try:
            func = getattr(module, method)
            return_value = func(*args)
            print(f"function return value: {return_value} | type: {type(return_value)}")
        except BaseException as e:
            print(e)
        print()