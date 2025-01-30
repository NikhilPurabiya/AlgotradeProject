import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

class TrailingStopLossBacktest:
    def __init__(self, symbol, start_date, end_date, cash):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.cash = cash
        self.position = 0
        self.highest_price = 0
        self.entry_price = 0
        self.stop_price = 0
        self.last_exit_time = datetime.min
        self.trades = []

    def fetch_data(self):
        print(f"Fetching data for {self.symbol} from {self.start_date} to {self.end_date}")
        data = yf.download(self.symbol, start=self.start_date, end=self.end_date, interval="1d")  # Use daily data
        data['Date'] = data.index
        return data

    def backtest(self):
        data = self.fetch_data()
        data['Position'] = 0
        for index, row in data.iterrows():
            current_time = row['Date']
            current_price = row['Close']

            # Wait 30 days after last exit
            if (current_time - self.last_exit_time).days < 30:
                continue

            # Entry condition: Enter position if not invested
            if self.position == 0:
                self.position = self.cash // current_price
                self.entry_price = current_price
                self.cash -= self.position * self.entry_price
                self.highest_price = current_price
                self.stop_price = current_price * 0.95
                self.trades.append((current_time, "BUY", self.position, current_price))
                print(f"{current_time}: BUY {self.position} shares at ${current_price:.2f}")
                data.loc[index, 'Position'] = 1  # Mark entry

            # Update trailing stop-loss
            if self.position > 0:
                if current_price > self.highest_price:
                    self.highest_price = current_price
                    self.stop_price = self.highest_price * 0.95

                # Exit condition: Trigger stop-loss
                if current_price <= self.stop_price:
                    self.cash += self.position * current_price
                    self.trades.append((current_time, "SELL", self.position, current_price))
                    print(f"{current_time}: SELL {self.position} shares at ${current_price:.2f}")
                    self.position = 0
                    self.last_exit_time = current_time
                    data.loc[index, 'Position'] = -1  # Mark exit

        # Final portfolio value
        if self.position > 0:
            self.cash += self.position * current_price
            print(f"Final Sell: {current_price:.2f}")
        print(f"Final Cash: ${self.cash:.2f}")
        self.visualize(data)

    def visualize(self, data):
        # Plot price and trades
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'], data['Close'], label='Price', color='blue', alpha=0.6)
        
        # Mark buy and sell points
        buys = data[data['Position'] == 1]
        sells = data[data['Position'] == -1]
        plt.scatter(buys['Date'], buys['Close'], color='green', label='Buy', marker='^', alpha=1)
        plt.scatter(sells['Date'], sells['Close'], color='red', label='Sell', marker='v', alpha=1)
        
        plt.title(f"Trailing Stop Loss Backtest for {self.symbol}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.show()

if __name__ == "__main__":
    strategy = TrailingStopLossBacktest(
        symbol="QQQ",  # Stock symbol
        start_date="2018-01-01",  # Start date
        end_date="2021-01-01",  # End date
        cash=100000  # Initial cash
    )
    strategy.backtest()
