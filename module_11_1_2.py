import numpy as np
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame


def repl(s:str):
    return s.replace('\n','')

if __name__ == '__main__':
    mtrx = {}
    df = {}
    cols = []
    idxs = set([])
    for i in range(2021, 2025):
        # with open(f'.\\Data\\col_zakdog{i}.csv', 'r') as f:
        #     lines = f.readlines()
        # lines = [l_[:-1] for l_ in lines]
        # mtrx[2000+i] = np.empty()  #array(lines[0].split(';'))
        # for j in range(1,len(lines)):
        #     mtrx[2000+i] = np.append(mtrx[2000+i], lines[j].split(';'), axis=0)
        # mtrx[i] = np.genfromtxt(fname=f'.\\Data\\col_zakdog{i}.csv',dtype=int,delimiter=';',)
        df[i] = pd.read_csv(filepath_or_buffer=f'.\\Data\\col_zakdog{i}.csv',delimiter=';'
                              , encoding='cp1251', dtype={0:str},index_col=0)
        # mtrx[i] = df[i].values
        # print(f'{i}, {mtrx[i]}')
        if len(cols) < len(df[i].columns):
            cols = df[i].columns
        idxs = idxs.union(set(df[i].index))

print(cols)
print(idxs)

gr = {}

for i in idxs:
    gr[i] = pd.DataFrame(index=range(2021,2025),columns=cols, dtype=int)
    for y in range(2021,2025):
        try:
            gr[i].loc[y] = df[y].loc[i]
        except KeyError :
            pass
    print(f'\nContract type: {i}')
    print(gr[i])
# for i =
# print(df[2021].columns)
# delivery = pd.DataFrame(index=range(2021,2025), columns=df[2021].columns)
# for i in range(2021,2025):
#     delivery.loc[i] = df[i].loc['Роды']
#
# print(delivery)




