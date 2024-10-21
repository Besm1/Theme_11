import numpy as np
import pandas as pd

def repl(s:str):
    return s.replace('\n','')

if __name__ == '__main__':
    mtrx = {}
    for i in range(2021, 2025):
        mtrx[i] = pd.read_csv(filepath_or_buffer=f'.\\Data\\col_zakdog{i}.csv',delimiter=';'
                              ,index_col=0, encoding='cp1251', dtype=int).values
        print(f'{i}, {mtrx[i]}')
