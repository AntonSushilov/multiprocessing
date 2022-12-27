from multiprocessing import Pool, cpu_count
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
    print("Задание завершено")
    # print(response)
    save_data(response)


def get_value(value):
    # print(value)
    return value.upper()


def get_value_star_async(value1, value2, value3):
    # print(str(value1)+str(value2)+str(value3))
    return str(value1)+str(value2)+str(value3)


def pool_map_proc(data):
    with Pool(cpu_count()) as p:
        p.map(get_value, data)
        p.close()
        p.join()


def pool_map_async_proc(data):
    with Pool(cpu_count()) as p:
        p.map_async(get_value, data, callback=callback_func)
        p.close()
        p.join()


def pool_map_apply_async(data):
    # Возврат одного элемента из callback
    with Pool(cpu_count()) as p:
        for i in range(len(data)):
            p.apply_async(get_value, args=(data[i],), callback=callback_func)
        p.close()
        p.join()


def pool_mapstar_async(data):
    with Pool(cpu_count()) as p:
        # Нужен список из кортежей
        p.starmap_async(get_value_star_async, data, callback=callback_func)
        p.close()
        p.join()


if __name__ == "__main__":
    RES_LIST = []
    path = "test.txt"
    data = get_data(path)

    pool_map_apply_async(data)
    pool_mapstar_async([(1,2,3),(4,5,6)])
    save_data(RES_LIST, path="RES_LIST.txt")
    print(cpu_count())