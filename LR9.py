import graphviz
from graphviz import Digraph
class Trader:
    def __init__(self, name):
        self.name = name

    def request_loan(self, trading_system, amount, terms):
        print(f"{self.name} запитує позику: {amount} з умовами {terms}")
        trading_system.create_order(amount, terms)

class TradingSystem:
    def __init__(self):
        self.order = None

    def create_order(self, amount, terms):
        print(f"TradingSystem створює боргову угоду на суму {amount} з відсотками {terms}")
        self.order = Order(amount, terms)
        self.order.reserve_funds()

class Order:
    def __init__(self, amount, interest):
        self.amount = amount
        self.interest = interest

    def reserve_funds(self):
        print(f"Order резервує кошти на суму {self.amount} з відсотками {self.interest}")
        stock_exchange = StockExchange()
        stock_exchange.provide_loan(self)

class StockExchange:
    def provide_loan(self, order):
        print(f"StockExchange надає позичені кошти: {order.amount}")
        trader = Trader("Трейдер")
        trader.receive_loan(order)

    def close_debt(self, order):
        print(f"StockExchange закриває борг на суму {order.amount + order.interest}")
        order.update_status()

class Module:
    def return_debt(self, order):
        print(f"Module повертає борг на суму {order.amount + order.interest}")
        stock_exchange = StockExchange()
        stock_exchange.close_debt(order)

    def update_status(self):
        print(f"Order оновлює статус боргу")

# Демонстрація роботи
trader = Trader("Трейдер")
trading_system = TradingSystem()

# Трейдер бере позику
trader.request_loan(trading_system, 1000, 10)

# Трейдер повертає борг
module = Module()
module.return_debt(trading_system.order)
