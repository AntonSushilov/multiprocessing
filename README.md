# Multiprocessing
Проект с примерами использования Multiprocessing в Python

## Содержание
- [Описание проекта](#описание-проекта)
- [Примеры](#примеры)
- [Установка](#установка)
- [Ссылки](#ссылки)

## Описание проекта
Этот репозиторий содержит пример многопроцессорного программирования на Python с использованием модуля multiprocessing для создания параллельных процессов и управления ресурсами между ними.

## Примеры
1. `example_manager.py`: работа с пулом процессов, используя класс `Manager()` модуля `multiprocessing`. Он возвращает запущенный объект SyncManager, который можно использовать для совместного использования объектов между процессами.
Возвращенный объект-менеджер SyncManager соответствует порожденному дочернему процессу и имеет методы, которые будут создавать общие объекты и возвращать соответствующие прокси объекты.
Процессы диспетчера будут завершены, как только они будут собраны сборщиком мусора или их родительский процесс завершится.
2. `example_manager.py`: примеры использования методов класса `Pool()`
3. `example_process.py`: пример с использованием `Manager()`, `Process()`, `Queue()`, `RLock`
Нуждается в рефакторинге



## Ссылки
Необходимое импортировать с помощью `from multiprocessing import`

1. [Manager()](https://docs-python.ru/standart-library/paket-multiprocessing-python/klass-manager-modulja-multiprocessing/)
2. [Pool()](https://docs-python.ru/standart-library/paket-multiprocessing-python/klass-pool-modulja-multiprocessing/)
    - [Pool.apply()](https://superfastpython.com/multiprocessing-pool-apply/)
    - [Pool.apply_async()](https://superfastpython.com/multiprocessing-pool-apply_async/)
    - [Pool.map()](https://superfastpython.com/multiprocessing-pool-map/)
    - [Pool.map_async()](https://superfastpython.com/multiprocessing-pool-map_async/)
    - [Pool.imap()](https://superfastpython.com/multiprocessing-pool-imap/)
    - [Pool.imap_unordered()](https://superfastpython.com/multiprocessing-pool-imap_unordered/)
    - [Pool.starmap()](https://superfastpython.com/multiprocessing-pool-starmap/)
    - [Pool.starmap_async()](https://superfastpython.com/multiprocessing-pool-starmap_async/)