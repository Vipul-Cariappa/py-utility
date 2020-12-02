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


def memoryit(func):
    """decorator function to measures the peak memory consumption of given function

    Args:
        func (`function`): function to execute

    Return:
        peak memory used during the execution of given function in bytes (`int`)
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
