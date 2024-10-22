""""
Задача.
Имеются файлы типа MS Excel с годовыми отчётами некой коммерческой  медицинской организации по помесячному количеству
заключённых договоров в разрезе их типов:

        янв фев мар апр ....
  тип1  n11 n12 n13 n14 ...
  тип2  n21 n22 n23 n24 ...
   ...  ... ... ... ... ...
  ИТОГО T1 T2  T3  T4   ...

Необходимо собрать данные со всех имеющихся файлов по трём типам договоров (ведение родов, ведение беременности, детские
и госпитализация). В результате надо получить три графика, по одному на каждый из трёх типов договоров. Ось ординат - года,
ось абсцисс - суммарное количество заключенных договоров за весь период с января по последний месяц в самом "коротком"
файле.
("Самым коротким" может быть файл за текущий год, т.к. в нём в общем случае присутствуют данные только с января
по прошлый (полностью завершённый) месяц. Таким образом на графиках будет наглядно видна тенденция изменения количества
договоров за аналогичные периоды лет, представленных в отчётах.)

Файлы имеют наименования col_zakdogNNNN.xlsx, где NNNN - четырёхзначный номер года, за который представлен отчёт.
Количество файлов и годы, за которые представлены отчёты, заранее не известны, известно только, что медицинское
учреждение на рынке с 2011 года.

"""

import pandas as pd
import matplotlib.pyplot as plt

YEAR_1ST = 2018
YEAR_LAST = 2024 + 1

def get_key(t_:tuple):
    return t_[1]

if __name__ == '__main__':
    mtrx = {}
    df = {}
    cols = []
    idxs = []
    for i in range(YEAR_1ST, YEAR_LAST):
        with pd.ExcelFile(f'.\\Data\\col_zakdog{i}.xlsx') as xls:
            df[i] = pd.read_excel(io=xls, sheet_name=xls.sheet_names[0], index_col=(0,1), header=5)
        # print(f'Год: {i}')
        # print(df[i])
        if len(cols) == 0 or len(cols) > len(df[i].columns):
            cols = df[i].columns
        idxs.extend(df[i].index)


idx = list(set([get_key(i_) for i_ in idxs ]))
idxs = list(zip([pd.NA]*len(idx), idx))

gr = {} # fOR DIAGRAMS
grs = {}

for i in idxs:
    if i[1] in('Роды', 'Ведение беременности', 'Госпитализация', 'Детство'):
        gr[i] = pd.DataFrame(index=range(YEAR_1ST, YEAR_LAST),columns=cols, dtype=int)
        grs[i] = pd.DataFrame(index=range(YEAR_1ST, YEAR_LAST), columns=['Всего'], dtype=int)
        for y in range(YEAR_1ST, YEAR_LAST):
            try:
                gr[i].loc[y] = df[y].astype(dtype=int,copy=True).loc[i]

                grs[i].loc[y] = sum(df[y].astype(dtype=int,copy=True).loc[i])
            except KeyError :
                pass
        print(f'\nContract type: {i}')
        print(gr[i])
        print(grs[i])

        grs[i].plot.line()
        # gr[i].transpose().plot.bar(stacked=True)
        plt.title(label=i[1])
        plt.show()
