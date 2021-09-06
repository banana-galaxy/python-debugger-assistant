def RaiseADivisionError():
    def inner():
        def another_inner():
            def actual_func():
                return 1 / (1 - 1)

            return actual_func()

        return another_inner()

    return inner()


def hi():
    return {"hello": 123, "dorime": ["item1", "item2", "cheemsadidas", {"hello!": 1}]}


class Hey:
    pass


def my_func():
    return Hey()
