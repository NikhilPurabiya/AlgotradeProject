import yfinance as yf
import matplotlib.pyplot as plt
from collections import deque

class GapReversalAlgo:
    def __init__(self):
        self.cash = 100000
        self.position = 0
        self.rollingWindow = deque(maxlen=2)
        self.trades = []  # To store trade actions

    def backtest(self, start_date, end_date, symbols):
        data = {}
        for symbol in symbols:
            # Download data for each symbol with daily resolution
            data[symbol] = yf.download(symbol, start=start_date, end=end_date, interval="1d")
        
        for symbol in symbols:
            self.run_backtest_for_symbol(symbol, data[symbol])

        self.plot_results(data)

    def run_backtest_for_symbol(self, symbol, data):
        for date, row in data.iterrows():
            self.CustomBarHandler(row)

            if not self.rollingWindowReady():
                continue

            # Ensure scalar extraction for prev_close and open_price
            prev_close = self.rollingWindow[-1]['Close']  # This is a scalar (float)
            open_price = row['Open']  # This is already a scalar

            # Check if prev_close and open_price are floats
            if isinstance(prev_close, float) and isinstance(open_price, float):
                if open_price >= 1.01 * prev_close:  # Gap up
                    self.SetHoldings(symbol, -1, date, open_price)
                elif open_price <= 0.99 * prev_close:  # Gap down
                    self.SetHoldings(symbol, 1, date, open_price)

            self.ExitPositions(date, row['Close'])

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
        plt.figure(figsize=(14, 7))
        
        # Loop over all symbols' data (if data is a dictionary of symbols -> DataFrames)
        for symbol, df in data.items():
            trade_dates = [trade[0] for trade in self.trades if trade[1] == symbol]
            trade_prices = [trade[2] for trade in self.trades if trade[1] == symbol]
            actions = [trade[1] for trade in self.trades if trade[1] == symbol]

            plt.plot(df.index, df['Close'], label=f'{symbol} Close Price')
            for date, price, action in zip(trade_dates, trade_prices, actions):
                color = 'green' if action == "Buy" else 'red'
                plt.scatter(date, price, color=color, label=f'{action} {symbol}', zorder=5)

        plt.legend()
        plt.title('Gap Reversal Strategy Trades')
        plt.show()

if __name__ == "__main__":
    algo = GapReversalAlgo()
    algo.backtest(symbols=['AAPL', 'MSFT', 'GOOG'], start_date='2019-01-01', end_date='2021-01-01')
