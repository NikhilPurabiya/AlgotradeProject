import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import timedelta

class SimpleTradingAlgorithm:
    def __init__(self):
        self.data = self.load_data()
        self.cash = 100000  # Starting cash
        self.position = 0   # Current position (number of shares)
        self.entry_price = 0
        self.period = timedelta(days=31)
        self.next_entry_time = None
        self.buy_dates = []
        self.sell_dates = []
        self.buy_prices = []
        self.sell_prices = []

    def load_data(self):
        # Fetch historical data for SPY from Yahoo Finance
        ticker = "SPY"
        start_date = "2020-01-01"
        end_date = "2021-01-01"
        print(f"Fetching data for {ticker} from {start_date} to {end_date}")
        
        data = yf.download(ticker, start=start_date, end=end_date)
        data["daily_ret"] = data["Close"].pct_change()
        return data

    def run_strategy(self):
        for date, row in self.data.iterrows():
            price = row["Close"].item()  # Convert the 'Close' value to a float

            # Check if we are allowed to make a trade
            if self.next_entry_time and date < self.next_entry_time:
                continue

            # Entry condition: Buy if we are not invested
            if self.position == 0:
                self.buy(price, date)

            # Exit condition: Sell if price increases or decreases by 10%
            elif self.entry_price * 1.1 < price or self.entry_price * 0.9 > price:
                self.sell(price, date)

    def buy(self, price, date):
        shares = int(self.cash // price)  # Ensure shares is an integer
        self.position += shares
        self.cash -= shares * price
        self.entry_price = price
        self.next_entry_time = date + self.period
        self.buy_dates.append(date)
        self.buy_prices.append(price)
        print(f"{date.strftime('%Y-%m-%d')}: BUY {shares} shares at ${price:.2f}")

    def sell(self, price, date):
        self.cash += self.position * price
        self.sell_dates.append(date)
        self.sell_prices.append(price)
        print(f"{date.strftime('%Y-%m-%d')}: SELL {self.position} shares at ${price:.2f}")
        self.position = 0
        self.entry_price = 0
        self.next_entry_time = date + self.period

    def plot_results(self):
        # Plot stock price and buy/sell points
        plt.figure(figsize=(10, 6))
        plt.plot(self.data.index, self.data["Close"], label="SPY Price", color="blue")

        # Plot Buy and Sell markers
        plt.scatter(self.buy_dates, self.buy_prices, marker="^", color="g", label="Buy", alpha=1)
        plt.scatter(self.sell_dates, self.sell_prices, marker="v", color="r", label="Sell", alpha=1)

        # Formatting the plot
        plt.title("Simple Trading Algorithm - Buy/Sell Strategy")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.legend(loc="best")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    algo = SimpleTradingAlgorithm()
    algo.run_strategy()
    print(f"Final Cash: ${algo.cash:.2f}")
    algo.plot_results()

