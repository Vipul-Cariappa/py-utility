import tracemalloc as tm
import multiprocessing as mp
import resource


def me_worker(func, storage, *args, **kwargs):
    """measures the peak memory consumption of given function; should be run by memoryit decorator as a new process

    Args:
        func (`function`): function to execute
        storage (`list`): multiprocessing.Manager().List() to store the peak memory
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        peak memory used during the execution of given function in bytes (`int`)
    """

    tm.start()
    now_mem, peak_mem = tm.get_traced_memory()

    return_value = func(*args, **kwargs)

    new_mem, new_peak = tm.get_traced_memory()
    tm.stop()

    storage.append(new_peak - now_mem)

    return new_peak - now_mem


def li_worker(func, limit, storage, *args, **kwargs):
    """limits the memory consumption of given function; should be run by limit_memory decorator as a new process

    Args:
        func (`function`): function to execute
        limit (`int`): maximum allowed memory consuption
        storage (`list`): multiprocessing.Manager().List() to store the peak memory
        args (`tuple`): arguments for the function
        kwargs(`dict`): keyword arguments for the function

    Return:
        return value of function or MemoryError
    """
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS,
                       (int(limit * 1024 * 1024), hard))

    try:
        value = func(*args, **kwargs)
        storage.append(value)
    except Exception as error:
        storage.append(error)
    finally:
        resource.setrlimit(resource.RLIMIT_AS, (soft, hard))

    return 0


def memoryit(func):
    """decorator function to measures the peak memory consumption of given function

    Args:
        func (`function`): function to execute

    Return:
        peak memory used during the execution of given function in bytes (`int`)
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


def limit_memory(value=15):
    """decorator function to limits the memory consumption of given function

    Args:
        value (`int`): maximum allowed memory consuption in MB
        func (`function`): function to execute

    Return:
        return value of function or MemoryError
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            ctx = mp.get_context('spawn')
            manager = ctx.Manager()
            l = manager.list()
            p = ctx.Process(target=li_worker, args=(
                func, value, l, *args), kwargs=kwargs)
            p.start()
            p.join()

            if isinstance(l[-1], Exception):
                raise l[-1]
            else:
                return l[-1]

        return wrapper
    return decorator
