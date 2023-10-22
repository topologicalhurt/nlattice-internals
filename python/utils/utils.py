from time import time


def time_it(func):
    def wrapper():
        start = time()
        func()
        end = time()
        print(f'Completed with a final time of: {end - start}s')
    return wrapper
