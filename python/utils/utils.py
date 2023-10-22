from time import time


def time_it(func):
    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        end = time()
        print(f'Completed with a final time of: {end - start}s')
    return wrapper
