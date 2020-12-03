from time import time
import multiprocessing as mp
import tracemalloc as tm
import resource
import signal


def me_worker(func, storage, *args, **kwargs):
    """measures the peak memory consumption and time taken for execution of given function

    Args:
        func (`function`): function to execute
        storage (`list`): multiprocessing.Manager().List() to store the peak memory
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        peak memory used, time taken during the execution of given function in bytes (`list` of 'int', 'float')
    """

    tm.start()
    t1 = time()  # time start
    now_mem, peak_mem = tm.get_traced_memory()  # memory start

    value = func(*args, **kwargs)  # calling function

    new_mem, new_peak = tm.get_traced_memory()  # memory stop
    t2 = time()  # time stop
    tm.stop()

    storage.append(new_peak - now_mem)
    storage.append(t2-t1)

    return 0


def li_worker(func, storage, time, memory, *args, **kwargs):
    """limits the memory consumption and time taken to execute given function

    Args:
        func (`function`): function to execute
        storage (`list`): multiprocessing.Manager().List() to store the peak memory
        time (`int`): maximum allowed time in seconds
        memory (`int`): maximum allowed memory consumption in MB
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        return value of function or MemoryError or TimeoutError
    """

    # setting time limit
    def signal_handler(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(time)

    # setting memory limit
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS,
                       (int(memory * 1024 * 1024), hard))

    # running the function
    try:
        value = func(*args, **kwargs)
        storage.append(value)
    except Exception as error:
        storage.append(error)
    finally:
        resource.setrlimit(resource.RLIMIT_AS, (soft, hard))
        signal.alarm(0)

    return 0


def measureit(func):
    """decorator function to measures the peak memory consumption and time taken to execute given function

    Args:
        func (`function`): function to execute

    Return:
        peak memory used, time taken during the execution of given function in bytes (`tuple` of 'int', 'float')
    """
    def wrapper(*args, **kwargs):
        ctx = mp.get_context('spawn')
        manager = ctx.Manager()
        com_obj = manager.list()
        p = ctx.Process(target=me_worker, args=(
            func, com_obj, *args), kwargs=kwargs)
        p.start()
        p.join()

        if len(com_obj) == 2:
            return tuple(com_obj)

        # else
        raise com_obj[-1]

    return wrapper


def limit_resource(time=10, memory=25):
    """decorator function to limits the memory consumption and time taken to execute given function

    Args:
        time (`int`): maximum allowed time consuption in seconds
        memory (`int`): maximum allowed memory consuption in MB
        func (`function`): function to execute

    Return:
        return value of function or MemoryError or TimeoutError
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            ctx = mp.get_context('spawn')
            manager = ctx.Manager()
            com_obj = manager.list()
            p = ctx.Process(target=li_worker, args=(
                func, com_obj, time, memory, *args), kwargs=kwargs)
            p.start()
            p.join()

            if isinstance(com_obj[-1], Exception):
                raise com_obj[-1]
            else:
                return com_obj[-1]

        return wrapper
    return decorator
