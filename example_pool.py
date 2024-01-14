from multiprocessing import Pool, cpu_count, current_process
import time, random
# import pandas as pd
# import os


def get_data(path="test.txt"):
    with open(path, 'r') as f:
        data = f.read()

    return data.split('\n')


def save_data(data, path="res_test.txt"):
    if isinstance(data, list):
        with open(path, 'w') as f:
            f.writelines('\n'.join(data))
    else:
        global RES_LIST
        RES_LIST.append(data)


def callback_func(response):
    print(f"Задание завершено {response}")
    # print(response)
    # save_data(response)

def error_callback_func(error):
    print(f'Got an Error: {error}')


def get_value(value):
    # print(value)
    return value.upper()


def worker_save(data):
    print(current_process().pid, current_process().name)
    print("worker save start")
    time.sleep(random.randint(0, 3))
    print("worker save end")
    return "save ok"


def worker(value):
    # print(value)
    print(current_process().pid, current_process().name)
    time.sleep(random.randint(0, 3))
    return value.upper()


def worker_starmap(*args):
    # print(str(value1)+str(value2)+str(value3))
    return "".join([arg.upper() for arg in args])


def get_value_star_async(value1, value2, value3):
    # print(str(value1)+str(value2)+str(value3))
    return str(value1)+str(value2)+str(value3)


def pool_apply_proc(data, max_pools):
    """
    Pool.apply() - одноразовая задача пулу процессов
    Вызов будет заблокирован до тех пор, 
    пока функция не будет выполнена рабочим процессом,
    после чего произойдет возврат.

    Например с помощью этой задачи можно сохранять промежуточные результаты
    """

    # example 1
    p = Pool()
    res = p.apply(worker_save, args=(data,))
    print('result: ', res)
    p.close()

    # example 2
    with Pool(max_pools) as p:
        res = p.apply(worker_save, args=(data,))
        print('result: ', res)
        res = p.apply(worker_save, args=(data,))
        print('result: ', res)
        p.close()
        p.join()


def pool_apply_async_proc(data, max_pools):
    """
    Pool.apply() - одноразовая задача пулу процессов
    Вызов не будет заблокирован.

    """

    # example 1
    p = Pool()
    res = p.apply_async(worker, args=("data", ), callback=callback_func)
    print('result: ', res)
    p.close()
    p.join()

    # example 2
    with Pool(max_pools) as p:
        res = p.apply_async(worker, args=("data",), callback=callback_func)
        print('result: ', res)
        res = p.apply_async(worker, args=("data"), callback=callback_func, error_callback=error_callback_func)
        print('result: ', res)
        p.close()
        p.join()

    # example 3
    with Pool(max_pools) as p:
        for i in range(len(data)):
            p.apply_async(get_value, args=(data[i],), callback=callback_func)
        p.close()
        p.join()


def pool_map_proc(data, max_pools):
    """
    Pool.map() применяет заданную функцию к каждому элементу в данной итерации параллельно
    Pool.map() возвращает результат с сохранением порядка вызова заданной функции для эелементов
    """
    # example 1
    time_start = time.time()
    with Pool(max_pools) as p:
        res = p.map(worker, data, chunksize=1)
        p.close()
        p.join()
    print(f"ex 1. worker time: {time.time() - time_start}")
    
    # example 2
    time_start = time.time()
    with Pool(max_pools) as p:
        res = p.map(worker, data, chunksize=5)
        p.close()
        p.join()
    print(f"ex 2. worker time: {time.time() - time_start}")


def pool_map_async_proc(data, max_pools):
    """
    Pool.map_async() применяет заданную функцию к каждому элементу в данной итерации асинхронно
    Pool.map_async() возвращает результат с сохранением порядка вызова заданной функции для эелементов
    """
    # example 1
    time_start = time.time()
    with Pool(max_pools) as p:
        res = p.map_async(worker, data, callback=callback_func, chunksize=1)
        p.close()
        p.join()
    print(f"ex 1. worker time: {time.time() - time_start}")

    # example 2
    time_start = time.time()
    with Pool(max_pools) as p:
        res = p.map_async(worker, data, callback=callback_func, error_callback=error_callback_func, chunksize=5)
        p.close()
        p.join()    
    print(f"ex 2. worker time: {time.time() - time_start}")


def pool_imap_proc(data, max_pools):
    """
    """
    # example 1
    time_start = time.time()
    with Pool(max_pools) as p:
        for res in p.imap(worker, data):
            print(res)
        p.close()
        p.join()
    print(f"ex 1. worker time: {time.time() - time_start}")
    time_start = time.time()
    # example 2
    time_start = time.time()
    with Pool(max_pools) as p:
        for res in p.imap(worker, data, chunksize=5):
            print(res)
        p.close()
        p.join()
    print(f"ex 2. worker time: {time.time() - time_start}")
    time_start = time.time()


def pool_imap_unordered_proc(data, max_pools):
    """
    """
    # example 1
    time_start = time.time()
    with Pool(max_pools) as p:
        for res in p.imap_unordered(worker, data):
            print(res)
        p.close()
        p.join()
    print(f"ex 1. worker time: {time.time() - time_start}")
    time_start = time.time()
    # example 2
    time_start = time.time()
    with Pool(max_pools) as p:
        for res in p.imap_unordered(worker, data, chunksize=5):
            print(res)
        p.close()
        p.join()
    print(f"ex 2. worker time: {time.time() - time_start}")
    time_start = time.time()


def pool_starmap_proc(data, max_pools):
    """
    """
    # example 1
    time_start = time.time()
    with Pool(max_pools) as p:
        for res in p.starmap(worker_starmap, data):
            print(res)
        p.close()
        p.join()
    print(f"ex 1. worker time: {time.time() - time_start}")
    time_start = time.time()

    # example 2
    time_start = time.time()
    with Pool(max_pools) as p:
        for res in p.starmap(worker_starmap, data, chunksize=5):
            print(res)
        p.close()
        p.join()
    print(f"ex 2. worker time: {time.time() - time_start}")
    time_start = time.time()


def pool_starmap_async_proc(data, max_pools):
    """
    """
    # example 1
    time_start = time.time()
    with Pool(max_pools) as p:
        res = p.starmap_async(worker_starmap, data)
        for r in res.get():
            print(r)
        p.close()
        p.join()
    print(f"ex 1. worker time: {time.time() - time_start}")
    time_start = time.time()

    # example 2
    time_start = time.time()
    with Pool(max_pools) as p:
        res = p.starmap_async(worker_starmap, data)
        for r in res.get():
            print(r)
        p.close()
        p.join()
    print(f"ex 2. worker time: {time.time() - time_start}")
    time_start = time.time()

    # example 3
    time_start = time.time()
    with Pool(max_pools) as p:
        p.starmap_async(worker_starmap, data, callback=callback_func, error_callback=error_callback_func)
        p.close()
        p.join()
    print(f"ex 3. worker time: {time.time() - time_start}")
    time_start = time.time()


if __name__ == "__main__":
    RES_LIST = []
    path = "test.txt"
    data = get_data(path)
    max_pools = cpu_count()
    data = [
        "d", "a", "t", "a",
        "d", "a", "t", "a",
        "d", "a", "t", "a",
        "d", "a", "t", "a",
        "d", "a", "t", "a",
        "d", "a", "t", "a",
        ]
    starmap_data = [
        ("d", "a", "t", "a"),
        ("d", "a", "t", "a"),
        ("d", "a", "t", "a"),
        ("d", "a", "t", "a"),
        ("d", "a", "t", "a"),   
        ]
    # print(data)
    # pool_apply_proc(data, max_pools)
    # pool_apply_async_proc(data, max_pools)
    # pool_map_proc(data, max_pools)
    # pool_map_async_proc(data, max_pools)
    # pool_imap_proc(data, max_pools)
    # pool_imap_unordered_proc(data, max_pools)
    # pool_starmap_proc(starmap_data, max_pools)
    pool_starmap_async_proc(starmap_data, max_pools)
    
    # save_data(RES_LIST, path="RES_LIST.txt")
    print(cpu_count())