from multiprocessing import Process, Manager

def dothing(L, i):  # the managed list `L` passed explicitly.
    L.append("anything")

if __name__ == "__main__":
    with Manager() as manager:
        L = manager.list()  # <-- can be shared between processes.
        processes = []
        for i in range(5):
            p = Process(target=dothing, args=(L,i))  # Passing the list
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        print(L)