def min_arguments(num: int):
    def decorator(func):
        def inner(*args):
            if len(args) < num:
                raise TypeError(f"{func.__name__} expects at least {num} arguments. Got {len(args)}")
            return func(*args)
        return inner

    return decorator
