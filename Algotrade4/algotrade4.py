import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

class GapReversalAlgo:

    def __init__(self):
        self.cash = 100000
        self.position = 0
        self.rollingWindow = deque(maxlen=2)
        self.trades = []  # To store trade actions

    def backtest(self, start_date, end_date, symbol):
        # Fetch historical data
        data = yf.download(symbol, start=start_date, end=end_date, interval='1d')
        data = data[['Open', 'High', 'Low', 'Close']]

        for date, row in data.iterrows():
            self.CustomBarHandler(row)

            if not self.rollingWindowReady():
                continue

            # Ensure scalar extraction for prev_close and open_price
            prev_close = self.rollingWindow[-1]['Close']  # This should be a scalar (float)
            open_price = row['Open']  # This should also be a scalar (float)

            if isinstance(prev_close, pd.Series):
                prev_close = prev_close.item()  # Convert to scalar if it's a Series
            if isinstance(open_price, pd.Series):
                open_price = open_price.item()  # Convert to scalar if it's a Series

            if open_price >= 1.01 * prev_close:  # Gap up
                self.SetHoldings(symbol, -1, date, open_price)
            elif open_price <= 0.99 * prev_close:  # Gap down
                self.SetHoldings(symbol, 1, date, open_price)

            self.ExitPositions(date, row['Close'])

        self.plot_results(data)

    def rollingWindowReady(self):
        return len(self.rollingWindow) == self.rollingWindow.maxlen

    def CustomBarHandler(self, bar):
        self.rollingWindow.append(bar)

    def SetHoldings(self, symbol, position, date, price):
        if self.position != position:
            self.position = position
            action = "Buy" if position == 1 else "Sell"
            self.trades.append((date, action, price))

    def ExitPositions(self, date, price):
        if self.position != 0:
            self.trades.append((date, "Exit", price))
            self.position = 0

    def plot_results(self, data):
        # Extract trades for plotting
        trade_dates = [trade[0] for trade in self.trades]
        trade_prices = [trade[2] for trade in self.trades]
        actions = [trade[1] for trade in self.trades]

        plt.figure(figsize=(14, 7))
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        for date, price, action in zip(trade_dates, trade_prices, actions):
            color = 'green' if action == "Buy" else 'red'
            plt.scatter(date, price, color=color, label=action, zorder=5)

        plt.legend()
        plt.title('Gap Reversal Strategy Trades')
        plt.show()

if __name__ == "__main__":
    algo = GapReversalAlgo()
    algo.backtest(start_date='2018-01-01', end_date='2021-01-01', symbol='SPY')

