from multiprocessing import Process, current_process, active_children, Queue, Lock, Manager
import os
import time
import pandas as pd
import random
from tqdm import tqdm

def det_data(path, col_name=None):
    if col_name:
        return pd.read_excel(path)[col_name].to_list()
    else:
        return pd.read_excel(path)


def save_df(df, file_name, path):
    df.to_excel(os.path.join(path, file_name))


def creator_queue(data, q):
    print("Создание очереди")
    for item in tqdm(data, total=len(data)):
        q.put(item)
    print(q)
    print("Очередь создана")


def my_func(q, res_list, lock):
    while True:
        if q.empty():
            print(f'Queue is empty. {current_process().name} is close')
            break
        else:
            lock.acquire()
            try:
                print(f'start get data {current_process().name}')
                data = q.get()
                print(f"{current_process().name}")
                res_list.append(f"{current_process().name}. {data}")
                #time.sleep(int(current_process().name))
            except Exception as ex:
                print(f"Ошибка {ex}. {current_process().name}")
            finally:
                pass
                lock.release()

RES_LIST = []
if __name__ == "__main__":
    print(active_children())
    path = "test_file.xlsx"
    col_name = "Стих"
    data = det_data(path, col_name=col_name)
    #pd.DataFrame(columns=["text1", "text2"]).to_excel("df_res.xlsx", index=False)
    lock = Lock()
    q = Queue()
    proc_creator_queue = Process(target=creator_queue, args=(data, q), name="Process_creator_Qoueue", daemon=True)
    print(active_children())
    proc_creator_queue.start()
    print(active_children())
    proc_creator_queue.join()
    # while True:
    #     time.sleep(1)
    #     print(active_children())
    #     if len(active_children()) == 0:
    #         break

    processes = 3
    procs = []
    with Manager() as manager:
        res_list = manager.list()
        for index in range(processes):
            proc = Process(target=my_func, args=(q, res_list, lock), name=f"{index}", daemon=True)
            procs.append(proc)
            proc.start()

        q.close()
        q.join_thread()

        for proc in procs:
            proc.join()

        RES_LIST = list(res_list)
        print(RES_LIST)
        df = pd.DataFrame(columns=["text1", "text2"])
        df['text1'] = RES_LIST
        df.to_excel("df_res.xlsx", index=False)