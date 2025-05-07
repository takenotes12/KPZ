import pandas as pd
from pandas_ta import rsi, cci, macd, atr, adx, Series
import random
import os

# Створення папки для збереження, якщо ще не існує
output_dir = "project_results"
os.makedirs(output_dir, exist_ok=True)

# Вхідні дані
data = {
    'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', '2023-01-06'],
    'Close': [100, 102, 101, 103, 105, 107],
    'High': [101, 103, 102, 104, 106, 108],
    'Low':  [99, 100, 100, 102, 104, 106]
}
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Розрахунок індикаторів
df['RSI'] = rsi(df['Close'])
df['CCI'] = cci(df['High'], df['Low'], df['Close'])
macd_vals = macd(df['Close'])
df['MACD'] = macd_vals['MACD_12_26_9']
df['Signal_Line'] = macd_vals['MACDs_12_26_9']
df['MACD_Histogram'] = macd_vals['MACDh_12_26_9']
df['ATR'] = atr(df['High'], df['Low'], df['Close'])
df['ADX'] = adx(df['High'], df['Low'], df['Close'])['ADX_14']

# Видалення рядків з пропущеними значеннями
df.dropna(inplace=True)

# Аналіз індикаторів
def determine_meaning(row):
    rsi_v = row['RSI']
    cci_v = row['CCI']
    macd_hist = row['MACD_Histogram']

    # RSI and CCI signal
    rsi_signal = 'oversold' if rsi_v < 30 else 'overbought' if rsi_v > 70 else 'neutral'
    cci_signal = 'oversold' if cci_v < -100 else 'overbought' if cci_v > 100 else 'neutral'

    # MACD signal
    macd_signal = 'buy' if macd_hist > 0 else 'sell' if macd_hist < 0 else 'neutral'

    # Meaning logic
    if (rsi_signal == 'oversold' or cci_signal == 'oversold') and macd_signal == 'buy':
        return 'ціна буде рости'
    elif (rsi_signal == 'overbought' or cci_signal == 'overbought') and macd_signal == 'sell':
        return 'ціна буде падати'
    else:
        return 'ціна не зміниться'

df['meaning'] = df.apply(determine_meaning, axis=1)

# Підсумкова таблиця
result_df = df[['meaning', 'RSI', 'CCI', 'MACD']]

# Збереження до CSV
output_path = os.path.join(output_dir, "technical_indicators.csv")
result_df.to_csv(output_path, index=True)

print(f"[✓] Дані збережено до: {output_path}")
