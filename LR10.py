import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Trade:
    def __init__(self, entry_time, entry_price, stop_loss, take_profit):
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.exit_time = None
        self.exit_price = None
        self.PnL = None

    def close_trade(self, exit_time, exit_price):
        self.exit_time = exit_time
        self.exit_price = exit_price
        self.PnL = exit_price - self.entry_price  # для спрощення просто різниця цін

class Client:
    def __init__(self, data):
        self.data = data  # Приймемо, що дані передаються як pandas DataFrame

    def get_data(self):
        return self.data

class Backtester:
    def __init__(self, client, take_profit_length=20, stop_loss_length=10, initial_amount=1000):
        self.client = client
        self.amount = initial_amount
        self.take_profit_length = take_profit_length
        self.stop_loss_length = stop_loss_length
        self.balance = initial_amount
        self.trades = []
        self.current_position = None

    def run_backtest(self):
        data = self.client.get_data()
        for index, candle in enumerate(data.iterrows()):
            candle = candle[1]  # отримуємо рядок даних (candlestick)
            self.evaluate_conditions(candle, index, data)
        self.calculate_statistics()

    def evaluate_conditions(self, candle, index, data):
        # Умова входу в угоду (простий приклад)
        if candle['close'] > candle['open'] and self.balance >= 10:  # умовно
            # Відкриваємо угоду
            stop_loss = candle['close'] - self.stop_loss_length
            take_profit = candle['close'] + self.take_profit_length
            trade = Trade(candle['timestamp'], candle['close'], stop_loss, take_profit)
            self.trades.append(trade)
            self.current_position = trade  # зберігаємо поточну позицію
            print(f"Trade opened at {candle['timestamp']} with entry price {candle['close']}")

        # Умова виходу з угоди
        if self.current_position:
            if candle['low'] < self.current_position.stop_loss or candle['high'] > self.current_position.take_profit:
                self.current_position.close_trade(candle['timestamp'], candle['close'])
                print(f"Trade closed at {candle['timestamp']} with exit price {candle['close']}")
                self.balance += self.current_position.PnL  # оновлюємо баланс

    def calculate_statistics(self):
        total_PnL = sum([trade.PnL for trade in self.trades if trade.PnL is not None])
        total_trades = len(self.trades)
        win_trades = len([trade for trade in self.trades if trade.PnL > 0])
        win_rate = win_trades / total_trades if total_trades > 0 else 0

        print(f"Total trades: {total_trades}")
        print(f"Winning trades: {win_trades}")
        print(f"Win rate: {win_rate * 100}%")
        print(f"Total PnL: {total_PnL}")
        print(f"Final balance: {self.balance}")

class Statistics:
    def __init__(self, backtester):
        self.backtester = backtester

    def plot_balance(self):
        balances = [self.backtester.balance]  # можна додавати баланси за кожну свічку
        plt.plot(balances)
        plt.title("Balance over time")
        plt.show()

