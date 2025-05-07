pnl = sum(profits)  # Total profit/loss percentage
        max_drawdown = self.calculate_max_drawdown(profits)  # Maximum drawdown percentage
        return {"Profit Factor": pf, "Win Rate": wr, "PnL%": pnl, "Max Drawdown%": max_drawdown}

    # Calculate maximum drawdown
    def calculate_max_drawdown(self, profits):
        cumulative = np.cumsum(profits)
        peak = np.maximum.accumulate(cumulative)
        drawdown = (peak - cumulative) / peak
        return np.max(drawdown) * 100

# Function to generate synthetic (random) historical data
def load_data():
    dates = pd.date_range(start="2023-01-01", periods=100000, freq="T")  # Every minute
    prices = np.cumsum(np.random.randn(len(dates)) * 0.5) + 1000  # Random walk around 1000
    return pd.DataFrame({
        'time': dates,
        'open': prices,
        'high': prices + np.random.rand(len(dates)),
        'low': prices - np.random.rand(len(dates)),
        'close': prices,
        'volume': np.random.rand(len(dates))
    })

# Entry point
if name == "main":
    df = load_data()
    strategy = Strategy(tp_pct=0.03, sl_pct=0.015)  # Initialize strategy with custom TP and SL
    df = strategy.generate_indicators(df)  # Calculate indicators
    strategy.backtest(df)  # Run backtest
    stats = strategy.performance()  # Get performance results
    print(stats)
    
    # Plotting the results
    plt.figure(figsize=(12,6))
    
    # Plot the closing price
    plt.plot(df['time'], df['close'], label='Close Price', color='blue')
    
    # Plot buy/sell signals
    for trade in strategy.trades:
        if trade.side == 'LONG':
            plt.scatter(trade.entry_time, trade.entry_price, marker='^', color='green', label='Buy Signal' if trade == strategy.trades[0] else "")
            plt.scatter(trade.exit_time, trade.exit_price, marker='v', color='red', label='Sell Signal' if trade == strategy.trades[0] else "")
        elif trade.side == 'SHORT':
            plt.scatter(trade.entry_time, trade.entry_price, marker='v', color='red', label='Sell Signal' if trade == strategy.trades[0] else "")
            plt.scatter(trade.exit_time, trade.exit_price, marker='^', color='green', label='Buy Signal' if trade == strategy.trades[0] else "")
    
    plt.title('Price and Trade Signals')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='best')
    plt.show()
