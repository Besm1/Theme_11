from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

YEAR_1ST = 2011 # Дата выхода организации на рынок

def get_key(t_:tuple):
    """
    Для создания уникального набора двухуровневых индексов - вытаскивать только второй, значащий, уровень индекса
    """
    return t_[1]

if __name__ == '__main__':
    # df = {}     # Словарь DataFrame'ов: ключ - год, данные - DataFrame, считанный из файла
    cols = []   # Названия колонок
    idxs = []   # Уникальный набор индексов строк данных
    year = YEAR_1ST     # Счётчик годов, начинается с первого года работы учреждения
    year_cur = datetime.now().year      # Текущий год - последний из возможных отчётных
    with pd.ExcelFile(f'.\\Data\\col_zakdog2020.xlsx') as xls:
         df = pd.read_excel(io=xls, sheet_name=xls.sheet_names[0], header=5, index_col=0, usecols=lambda x: 'Unnamed' not in x,)
    print(df.index)
    print(df.columns)


# usecols=lambda x: 'Unnamed' not in x,