""""
Задача.
Имеются файлы типа MS Excel с годовыми отчётами некой коммерческой медицинской организации по помесячному количеству
заключённых договоров в разрезе их типов:

        янв фев мар апр ....
  тип1  n11 n12 n13 n14 ...
  тип2  n21 n22 n23 n24 ...
   ...  ... ... ... ... ...
  ИТОГО T1 T2  T3  T4   ...

Необходимо собрать данные со всех имеющихся файлов по четырём типам договоров (ведение родов, ведение беременности, детские
и госпитализация). В результате надо получить четыре графика, по одному на каждый из трёх типов договоров. Ось ординат - года,
ось абсцисс - суммарное количество заключенных договоров за весь период с января по последний месяц в самом "коротком"
отчёте.
("Самым коротким" может быть отчёт за текущий год, т.к. в нём в общем случае присутствуют данные только с января
по прошлый (полностью завершённый) месяц. Таким образом на графиках будет наглядно видна тенденция изменения количества
договоров за аналогичные периоды лет, представленных в отчётах.)

Файлы имеют наименования col_zakdogNNNN.xlsx, где NNNN - четырёхзначный номер года, за который представлен отчёт.
Количество файлов и годы, за которые представлены отчёты, заранее не известны, известно только, что медицинское
учреждение на рынке с 2011 года. Каждый отчёт лежит в первом рабочем листе книги Excel.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Комментарии разработчика (проблема уже неактуальна, но вопрос такой был!).
При внимательном изучении структуры исходных файлов видно, что данные начинаются не с первого столбца, первый
столбец пуст. В связи с этим много головной боли: метод pd.read_excel() не умеет пропускать столбцы, как
он это делает со строками, поэтому приходится "городить" двухуровневый индекс для грамотной обработки
наименований типов договоров. Поэтому индексы получаются не строковые, а определены в виде кортежей вида

        (NaN, '<тип договора>')

Как бы и ладно, если pd понимает такие индексы, так и пусть они в виде кортежей... Но после обработки всех файлов мне
нужен набор всевозможных типов договоров, которые только встречаются в отчётах, причём этот набор должен быть
уникальным. Вот тут-то и приходится мудрить: в случае с кортежами множество типа set не помогает исключить дубли -
ни один кортеж другому не равен...

Но, может, я какой-то секрет либо ещё не знаю, либо знаю, но не сообразил, как его для этой задачи применить.

Поэтому - ВОПРОС ПРОВЕРЯЮЩЕМУ, если он дочитал этот лонг-рид до этого места:
          ===================
Как можно и можно ли вообще дать понять pd.read_excel(), что первый столбец рабочего листа книги Excel вообще
игнорировать, а одноуровневый индекс собирать, начиная со второго столбца?

Ответ нашёл самостоятельно, даже два варианта, код переписал:
=============================================================
1. Можно в pd.read_excel() задать параметр usecols, в котором задать список (iterable) колонок, которые надо считывать
2. Можно указать, что не надо считывать те колонки, у которых нет заголовка. Для этого надо использовать специальное
   имя колонки = 'Unnamed' и использовать формулу:
        pd.read_excel(..., usecols=lambda x: 'Unnamed' not in x, index_col=0 )

"""

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import pprint

YEAR_1ST = 2011 # Дата выхода организации на рынок

if __name__ == '__main__':
    df = {}     # Словарь DataFrame'ов: ключ - год, данные - DataFrame, считанный из файла
    cols = []   # Названия колонок
    idxs = set([])   # Уникальный набор индексов строк данных
    year = YEAR_1ST     # Счётчик годов, начинается с первого года работы учреждения
    year_cur = datetime.now().year      # Текущий год - последний из возможных отчётных
    while year <= year_cur:
        try:
            with pd.ExcelFile(f'.\\Data\\col_zakdog{year}.xlsx') as xls:
                df[year] = pd.read_excel(io=xls, sheet_name=xls.sheet_names[0], header=5    # Пропустим 5 строк
                                            , usecols=lambda x: 'Unnamed' not in x, index_col=0 ) # и все колонки без заголовков
                # 'Unnamed' - это специальное псевдо-имя колонки, которое обозначает колонку без заголовка
            if len(cols) == 0 or len(cols) > len(df[year].columns): # 1) len(cols) == 0 -- условие инициализации индексов
                cols = df[year].columns                 # 2) len(cols) > len(...) -- это возможно только тогда, когда
                                                        #   текущий файл - самый "короткий", тогда список
                                                        #   используемых колонок берём из него
            idxs = idxs | set(df[year].index) # Добавляем все индексы из текущего файла -- вдруг какой-то новый тип договора
                                        #   в нём добавился. set() делает этот список уникальным.
        except FileNotFoundError:
            pass            # Файл за любой год может отсутствовать - это нормально
        finally:
            year += 1       # В любом случае - проверим следующий год

pprint.pprint(idxs)

gr = {} # DFs for diagrams - если графики помесячные закажут
grs = {}    # DFs с суммами по всем месяцам - для графика суммарных значений

for i in idxs:  # Индексы соответствуют названию договоров
    if i in('Роды', 'Ведение беременности', 'Госпитализация', 'Детство'):    # Обрабатываем только эти договоры
        # Готовим DataFrame'ы
        gr[i] = pd.DataFrame(index=list(df.keys()),columns=cols, dtype=int)     # Обрезаем колонки по длине cols
        grs[i] = pd.DataFrame(index=list(df.keys()), columns=['Всего'], dtype=int) # В суммарном - только одна колонка
        for y in df.keys(): # Перебираем по годам (это ключи набора матриц) исходных DF, данными наполняем DataFrame'ы
            try:
                gr[i].loc[y] = df[y].astype(dtype=int,copy=True).loc[i] # Это помесячный фрейм
                grs[i].loc[y] = sum(df[y].astype(dtype=int,copy=True).loc[i])   # Это фрейм итоговых сумм
            except KeyError:    # не во всех файлах есть все типы договоров
                pass
        print(f'\nContract type: {i}')
        print(grs[i])

        grs[i].plot.line()      # Подготавливаем линейный график
        # gr[i].transpose().plot.bar(stacked=True)  # Пробовал - не понравилось...
        plt.title(label=f'Договоры "{i}", годы с {grs[i].index[0]} по {grs[i].index[-1]}.')
        plt.show()  # Рисуем
