import pandas as pd

# Чтение данных с указанием типа индекса как строки
df = pd.read_csv(filepath_or_buffer=f'.\\Data\\col_zakdog2021.csv', delimiter=';', index_col=0, encoding='cp1251', dtype={0: str})

# Вывод DataFrame
print(df)

# Доступ к строкам по индексу
row = df.loc['БСК']
print(row)