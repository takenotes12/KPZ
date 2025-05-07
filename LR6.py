import pandas as pd
import matplotlib.pyplot as plt

# Завантаження даних з таблиці (припустимо, файл має назву 'rsi_data.csv')
# Формат CSV має вигляд: Дата,RSI_14,RSI_27,RSI_50
df = pd.read_csv('rsi_data.csv', parse_dates=['Дата'])

# Приклад побудови графіків для RSI з періодом 27
dates = df['Дата']
rsi_27 = df['RSI_27']

# Створення полотна з 3 підграфіками
plt.figure(figsize=(9, 3))

# bar - RSІ 27
plt.subplot(131)
plt.bar(dates, rsi_27)
plt.title('bar - RSI 27')
plt.xticks(rotation=45)

# scatter - RSІ 27
plt.subplot(132)
plt.scatter(dates, rsi_27)
plt.title('scatter - RSI 27')
plt.xticks(rotation=45)

# plot - RSІ 27
plt.subplot(133)
plt.plot(dates, rsi_27)
plt.title('plot - RSI 27')
plt.xticks(rotation=45)

# Автоматичне вирівнювання дати
plt.tight_layout()

# Збереження та показ графіку
plt.savefig('rsi_visualization.png')
plt.show()
