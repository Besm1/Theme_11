import inspect
from pprint import pprint
from requests import HTTPError
from threading import Lock


class Bank:
    def __init__(self, balance):
        self.balance = balance
        self.change_lock = Lock()
        self.take_lock = Lock()

    def deposit(self):
        for i in range(100):
            income = randint(50, 500)
            print(f'@1({i}): Запрос на пополнение {income}. Пытаемся закрыть замок change_lock...')
            self.change_lock.acquire()
            print(f'@1({i}): ... замок change_lock закрыт')
            self.balance += income
            print(f'@1({i}): Пополнение {income}. Баланс {self.balance}')
            sleep(0.001)     # Транзакция занимает время...
            print(f'@1({i}): Приход зафиксирован, открываем замок change_lock')
            self.change_lock.release()
            if self.take_lock.locked() and self.balance > 500:
                self.take_lock.release()
                print(f'@1({i}): Средств стало достаточно, открываем замок take_lock')
            # sleep(0.001)     # А это не время на транзакцию, а время между транзакциями... Непонятно, зачем.

    def take(self):
        for i in range(100):
            expense = randint(50,500)
            print(f'    @2({i}): Запрос на снятие {expense}.')
            if self.take_lock.locked() and not t1.is_alive():  # Если снятие залочено, а поступлений больше не будет
                self.take_lock.release()
            if self.balance >= expense:
                print(f'    @2({i}): Закрываем замок take_lock. Если не получилось - значит заблокировано по недостаче...')
                self.take_lock.acquire(timeout=0.000000001)
                # if not t1.is_alive():
                print(f'    @2({i}): ...замок take_lock закрыт!')
                print(f'    @2({i}): Закрываем замок change_lock. Если не получилось - значит сейчас происходит пополнение...')
                self.change_lock.acquire()
                print(f'    @2({i}): ...замок change_lock закрыт!')
                self.balance -= expense
                print(f'    @2({i}): Снятие {expense}. Баланс {self.balance}. Открываем замок change_lock.')
                self.change_lock.release()
                print(f'    @2({i}): Открываем замок замок take_lock!')
                if self.take_lock.locked():
                    self.take_lock.release()
            else:
                print(f'    @2({i}): Запрос отклонён, недостаточно средств (баланс {self.balance}).', end='')
                if t1.is_alive():
                    print(f'    @2({i}): Закрываем замок take_lock')
                    self.take_lock.acquire()
                    print(f'    @2({i}): замок take_lock закрыт!')
                else:
                    print(f'    @2({i}): Счёт арестован за недостачу!')
                    break



def introspection_info(obj):
    metadata = {}
    try:
        metadata['Name'] = obj.__name__
    except Exception:
        metadata['Name'] = None
    try:
        metadata['Module (__module__)'] = obj.__module__
    except Exception:
        metadata['Module (__module__)'] = None
    metadata['Module (getmodule)'] = inspect.getmodule(obj)
    metadata['Type'] = type(obj)
    metadata['Methods (public)'] = [memb for memb in dir(obj) if callable(getattr(obj, memb))
                                    and not memb.startswith('_')]
    metadata['Methods (dunder)'] = [memb for memb in dir(obj) if callable(getattr(obj, memb)) and memb.startswith('__')]
    metadata['Methods (private)'] = [memb for memb in dir(obj) if callable(getattr(obj, memb))
                                     and not memb.startswith('__') and memb.startswith('_')]
    metadata['Attributes (public)'] = [memb for memb in dir(obj) if not callable(getattr(obj, memb))
                                    and not memb.startswith('_')]
    metadata['Attributes (dunder)'] = [memb for memb in dir(obj) if not callable(getattr(obj, memb)) and memb.startswith('__')]
    metadata['Attributes (private)'] = [memb for memb in dir(obj) if not callable(getattr(obj, memb))
                                     and not memb.startswith('__') and memb.startswith('_')]
    metadata['Members (all)'] = inspect.getmembers(obj)
    metadata['Members (func)'] = inspect.getmembers(obj, predicate=inspect.isfunction)
    metadata['Members (meth)'] = inspect.getmembers(obj, predicate=inspect.ismethod)
    metadata['Callable'] = callable(obj)

    return metadata


print('\n\n*** Call: introspection_info(42)')
pprint(introspection_info(42))
print('\n\n*** Call: introspection_info(int)')
pprint(introspection_info(int))
print('\n\n*** Call: introspection_info(Bank)')
pprint(introspection_info(Bank))
print('\n\n*** Call: introspection_info(Bank())')
pprint(introspection_info(Bank(500)))
print('\n\n*** Call: introspection_info(inspect)')
pprint(introspection_info(inspect))
print('\n\n*** Call: introspection_info(HTTPError)')
pprint(introspection_info(HTTPError))
print('\n\n*** Call: introspection_info(introspection_info)')
pprint(introspection_info(introspection_info))


# help(inspect)