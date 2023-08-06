from timeit import default_timer as timer
from functools import wraps


def measure(func):
    @wraps(func)
    def time_it(*args, **kwargs):
        start = timer()
        try:
            return func(*args, **kwargs)
        finally:
            end = timer()
            print(f'Total execution time: {end - start:.8f} s')

    return time_it


def test():
    @measure
    def hello():
        print('hello world')

    hello()

if __name__ == '__main__':
    test()
