from datetime import datetime
import pandas as pd
import os

# Шлях до CSV-файлу
csv_path = 'datetime_log.csv'

# Колонки
columns = ['year', 'month', 'day', 'hour', 'minute', 'second']

# Отримуємо поточну дату та час
now = datetime.now()
new_row = {
    'year': now.year,
    'month': now.month,
    'day': now.day,
    'hour': now.hour,
    'minute': now.minute,
    'second': now.second
}

# Якщо файл існує — читаємо, інакше створюємо новий DataFrame
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=columns)

# Додаємо новий запис
df = df.append(new_row, ignore_index=True)

# Зберігаємо у файл
df.to_csv(csv_path, index=False)

print("Дата та час запуску додано до файлу.")
