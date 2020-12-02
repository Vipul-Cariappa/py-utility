from time import time
import multiprocessing as mp


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


def timeit(func):
    """decorator function to measure time taken to execute a given function in new process

    Args:
        func (`function`): function to execute

    Return:
        time taken to execute the given function in seconds (`int`)
    """
    def wrapper(*args, **kwargs):
        ctx = mp.get_context('fork')
        manager = ctx.Manager()
        l = manager.list()
        p = ctx.Process(target=me_worker, args=(
            func, l, *args), kwargs=kwargs)
        p.start()
        p.join()

        return l[-1]
    return wrapper
