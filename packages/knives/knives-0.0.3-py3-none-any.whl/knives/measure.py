import os
import psutil
import functools
import cProfile
from timeit import default_timer as timer

def second_to_human_friendly_time(seconds: float, precision: int=3) -> str:
    precision = 3 if precision < 1 or precision > 6 else precision
    days = int(seconds // (60*60*24))
    seconds %= 60*60*24
    hours = int(seconds // (60*60))
    seconds %= 60*60
    minutes = int(seconds // 60)
    seconds %= 60
    print(f'{days}d {hours:02}:{minutes:02}:{seconds:0>{precision+3}.{precision}f}')
    if days > 0:
        return f'{days}d {hours:02}:{minutes:02}:{seconds:0>{precision+3}.{precision}f}'
    elif hours > 0:
        return f'{hours:02}:{minutes:02}:{seconds:0>{precision+3}.{precision}f}'
    elif minutes > 0:
        return f'{minutes:02}:{seconds:0>{precision+3}.{precision}f}'
    else:
        return f'{seconds:.{precision}f}s'


def measure_time(func):
    @functools.wraps(func)
    def time_it(*args, **kwargs):
        start = timer()
        try:
            return func(*args, **kwargs)
        finally:
            end = timer()
            print(f'Time Usage for {func.__name__}(): {end - start:.8f} s')

    return time_it


def measure_profile(func):
    @functools.wraps(func)
    def profile_it(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        try:
            return func(*args, **kwargs)
        finally:
            pr.disable()
            print(f'[cProfile]:')
            pr.print_stats()

    return profile_it


def byte_to_human_friendly_size(bytes_number: int, precision: int=2) -> str:
    if bytes_number >= 1024**3:
        return f'{bytes_number/(1024**3):.{precision}f}GB'
    elif bytes_number >= 1024**2:
        return f'{bytes_number/(1024**2):.{precision}f}MB'
    elif bytes_number >= 1024**1:
        return f'{bytes_number/(1024**1):.{precision}f}KB'
    else:
        return f'{bytes_number}B'


def measure_memory(func):
    @functools.wraps(func)
    def check_memory(*args, **kwargs):
        process = psutil.Process(os.getpid())
        start = process.memory_info().rss
        try:
            return func(*args, **kwargs)
        finally:
            end = process.memory_info().rss
            print(f'Memory Usage: {byte_to_human_friendly_size(end - start)}')

    return check_memory

@measure_profile
def test():
    print(byte_to_human_friendly_size(1234567))
    print(second_to_human_friendly_time(1234.412))

if __name__ == '__main__':
    test()
