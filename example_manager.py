from multiprocessing import Process, Manager, current_process
import time, random
from tqdm import tqdm

def worker(lst, dkt, lock, task):  # the managed list `L` passed explicitly.
    """
    Функция для выполнения операции в процессе.

    Args:
        lst: Управляемый список, в который добавляются результаты.
        dkt: Управляемый словарь для использования в процессе.
        lock: Блокировщик для управления доступом к списку из других процессов.
        task: Значение для обработки.
    """
    pid_proc = current_process().pid
    proc_name = current_process().name
    # блокируем доступ к прокси-списку из других потоков 
    try:
        print(pid_proc, proc_name)
        time.sleep(random.randint(1,3))
        lock.acquire()
        lst.append(f"anything {task}")
        dkt[task] = proc_name
    finally:
        # завершаем процесс и разрешаем 
        # доступ к массиву другим процессам
        lock.release()
    


def main():
    """
    Основная функция для управления процессами и ресурсами.
    """
    tasks = range(10) # Задачи
    max_proc = 5 # максимальное число процессов для одновременного запуска
    with Manager() as manager: # Создаем менеджер контекста для управления ресурсами между процессами
        # создаем прокси список
        lst = manager.list()
        # создаем прокси словарь
        dkt = manager.dict()
        # создаем прокси блокировщик
        lock = manager.Lock()
        processes = []
        for i in tqdm(tasks, total=len(tasks)):
            p = Process(target=worker, args=(lst, dkt, lock, i))  # Passing the list
            p.start()
            processes.append(p)
            if len(processes) == max_proc:
                [proc.join() for proc in processes]
                print(len(lst))
                [proc.close() for proc in processes]
                processes = []
        print(lst)
        print(dkt)

if __name__ == "__main__":
    main()