from binance import Client
import pandas as pd
from datetime import datetime, timedelta

def calculate_rsi(asset: str, periods: list[int]) -> pd.DataFrame:
    # Підключення до Binance (без API ключів, тільки для публічних даних)
    client = Client()

    # Часовий діапазон: останні 24 години
    end_time = datetime.utcnow().replace(second=0, microsecond=0, minute=0)
    start_time = end_time - timedelta(days=1)

    # Отримання історичних свічок
    k_lines = client.get_historical_klines(
        symbol=asset,
        interval=Client.KLINE_INTERVAL_1MINUTE,
        start_str=start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_str=end_time.strftime("%Y-%m-%d %H:%M:%S")
    )

    # Перетворення у DataFrame
    df = pd.DataFrame(k_lines)[[0, 1, 2, 3, 4, 5]]
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['close'] = df['close'].astype(float)

    # Функція для обчислення RSI по заданому періоду
    def rsi(series: pd.Series, period: int) -> pd.Series:
        delta = series.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rsi = pd.Series(0.0, index=series.index)
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # Плавне EMA-обчислення, щоб відповідати формулі RSIn+1
        for i in range(period, len(series)):
            if i == period:
                avg_up = gain.iloc[:period].mean()
                avg_down = loss.iloc[:period].mean()
            else:
                avg_up = (avg_up * (period - 1) + gain.iloc[i]) / period
                avg_down = (avg_down * (period - 1) + loss.iloc[i]) / period
            rs = avg_up / avg_down if avg_down != 0 else 0
            rsi.iloc[i] = 100 - (100 / (1 + rs)) if rs != 0 else 100

        return rsi

    # Обчислення RSI для кожного з періодів
    for period in periods:
        df[f'RSI {period}'] = rsi(df['close'], period)

    # Залишаємо лише потрібні колонки
    return df[['time'] + [f'RSI {p}' for p in periods]]
