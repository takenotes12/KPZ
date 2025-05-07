from datetime import datetime
from dataclasses import dataclass

# Клас для сигналу
@dataclass
class Signal:
    time: datetime
    asset: str
    quantity: float
    side: str
    entry: float
    take_profit: float
    stop_loss: float
    result: float = "Proceed"

# Приклад стратегії
class TradingStrategy:
    def __init__(self, rsi_threshold=30, adx_threshold=35, take_profit_ratio=5/7, stop_loss_ratio=2/7):
        self.rsi_threshold = rsi_threshold
        self.adx_threshold = adx_threshold
        self.take_profit_ratio = take_profit_ratio
        self.stop_loss_ratio = stop_loss_ratio

    def create_signal(self, rsi, adx, current_price, asset, amount):
        # Перевірка сигналу на купівлю/продаж за допомогою RSI
        if rsi > 70:
            side = "SELL"
        elif rsi < 30:
            side = "BUY"
        else:
            return None  # Немає чіткого сигналу

        # Якщо ADX більше порогу, підтверджуємо сигнал
        if adx > self.adx_threshold:
            # Обчислюємо кількість монет для торгівлі
            quantity = round((1 - 0.02) * amount / current_price, 3)  # Знижка для можливої втрати

            # Розрахунок рівнів тейк-профіту та стоп-лоссу
            if side == "BUY":
                take_profit_price = round((1 + self.take_profit_ratio) * current_price, 1)
                stop_loss_price = round((1 - self.stop_loss_ratio) * current_price, 1)
            else:
                take_profit_price = round((1 - self.take_profit_ratio) * current_price, 1)
                stop_loss_price = round((1 + self.stop_loss_ratio) * current_price, 1)

            return Signal(
                time=datetime.now(),
                asset=asset,
                quantity=quantity,
                side=side,
                entry=current_price,
                take_profit=take_profit_price,
                stop_loss=stop_loss_price
            )
        else:
            return None  # ADX не підтверджує сигнал

# Функція моніторингу
def monitor(strategy, rsi_data, adx_data, current_price, asset, amount):
    while True:
        signal = strategy.create_signal(rsi=rsi_data, adx=adx_data, current_price=current_price, asset=asset, amount=amount)
        if signal:
            print(f"Signal generated: {signal}")
        else:
            print("No valid signal at this time.")

# Приклад використання
strategy = TradingStrategy()

# Припустимо, у нас є дані RSI та ADX
rsi = 25
adx = 40
current_price = 100  # поточна ціна
asset = "BTC"
amount = 1000  # баланс

# Моніторимо сигнали
monitor(strategy, rsi, adx, current_price, asset, amount)
