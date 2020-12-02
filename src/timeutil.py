from time import time
import multiprocessing as mp
import signal


def me_worker(func, storage, *args, **kwargs):
    """measures the time taken to execute given function should be run by timeit decorator as a new process

    Args:
        func (`function`): function to execute
        storage (`list`): multiprocessing.Manager().List() to store the time taken to excute
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        time taken to execute the given function in seconds (`int`)
    """
    t1 = time()
    return_value = func(*args, **kwargs)
    t2 = time()
    storage.append(t2-t1)
    return t2 - t1


def li_worker(func, time, storage, *args, **kwargs):
    """limits the time taken for exection of given function; should be run by limit_time decorator as a new process

    Args:
        func (`function`): function to execute
        limit (`int`): maximum allowed time in seconds
        storage (`list`): multiprocessing.Manager().List() to store the peak memory
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        return value of function or TimeoutError
    """
    def signal_handler(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(time)

    try:
        value = func(*args, **kwargs)
        storage.append(value)
    except Exception as error:
        storage.append(error)
    finally:
        signal.alarm(0)

    return 0


def timeit(func):
    """decorator function to measure time taken to execute a given function in new process

    Args:
        func (`function`): function to execute

    Return:
        time taken to execute the given function in seconds (`int`)
    """
    def wrapper(*args, **kwargs):
        ctx = mp.get_context('spawn')
        manager = ctx.Manager()
        l = manager.list()
        p = ctx.Process(target=me_worker, args=(
            func, l, *args), kwargs=kwargs)
        p.start()
        p.join()

        return l[-1]
    return wrapper


def limit_time(time=10):
    """decorator function to limits the time taken to execute given function

    Args:
        value (`int`): maximum allowed time in seconds
        func (`function`): function to execute

    Return:
        return value of function or TimeoutError
    """
    def inner(func):
        def wrapper(*args, **kwargs):

            ctx = mp.get_context('spawn')
            manager = ctx.Manager()
            l = manager.list()
            p = ctx.Process(target=li_worker, args=(
                func, time, l, *args), kwargs=kwargs)
            p.start()
            p.join()

            if isinstance(l[-1], Exception):
                raise l[-1]
            else:
                return l[-1]

        return wrapper
    return inner
