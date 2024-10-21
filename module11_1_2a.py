import numpy as np
import pandas as pd
from pandas.core.dtypes.missing import na_value_for_dtype
from pandas.core.interchange.dataframe_protocol import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.core.reshape.reshape import stack

YEAR_1ST = 2018
YEAR_LAST = 2025

def get_key(t_:tuple):
    return t_[1]

if __name__ == '__main__':
    mtrx = {}
    df = {}
    cols = []
    idxs = []
    for i in range(YEAR_1ST, YEAR_LAST):
        with pd.ExcelFile(f'.\\Data\\col_zakdog{i}.xlsx') as xls:
           df[i] = pd.read_excel(xls, xls.sheet_names[0], index_col=(0,1), header=5, skipfooter=1
                                    , usecols=[k for k in range(0,11)])
        print(f'Год: {i}')
        print(df[i][:10])
        if len(cols) < len(df[i].columns):
            cols = df[i].columns
        # idxs = idxs.union(df[i].index)
        idxs.extend(df[i].index)

idx = list(set([get_key(i_) for i_ in idxs ]))
idxs = list(zip([pd.NA]*len(idx), idx))

gr = {} # fOR DIAGRAMS
grs = {}

for i in idxs:
    if 'Роды' in i[1] or 'беременн' in i[1] or 'Госпитализ' in i[1]:
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
