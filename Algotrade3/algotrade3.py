import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime

class CustomSimpleMovingAverage:
    def __init__(self, period):
        self.period = period
        self.queue = deque(maxlen=period)
        self.Value = 0

    def Update(self, price):
        self.queue.append(price)
        self.Value = sum(self.queue) / len(self.queue) if len(self.queue) == self.queue.maxlen else None
        return self.IsReady()

    def IsReady(self):
        return len(self.queue) == self.queue.maxlen

def main():
    # Fetch historical SPY data from Yahoo Finance
    spy_data = yf.download('SPY', start='2020-01-01', end='2021-01-01', interval='1d')
    spy_data = spy_data[['Open', 'High', 'Low', 'Close']]
    spy_data.dropna(inplace=True)  # Ensure no missing data

    sma_period = 30
    sma = CustomSimpleMovingAverage(sma_period)

    highs, lows, smas, prices, dates = [], [], [], [], []

    for date, row in spy_data.iterrows():
        price = row['Close']
        sma.Update(price)

        if sma.IsReady():
            # Filter valid date range for history
            hist = spy_data.loc[spy_data.index <= date].iloc[-252:]  # Ensure no out-of-bound slicing
            if not hist.empty:  # Skip if history is empty
                high, low = hist['High'].max(), hist['Low'].min()

                highs.append(high)
                lows.append(low)
                smas.append(sma.Value)
                prices.append(price)
                dates.append(date)

    plt.figure(figsize=(14, 7))
    plt.plot(dates, prices, label='Price', color='blue')
    plt.plot(dates, highs, label='52w High', color='green')
    plt.plot(dates, lows, label='52w Low', color='red')
    plt.plot(dates, smas, label='SMA', color='orange')
    plt.legend()
    plt.title('SPY with SMA and 52-week High/Low')
    plt.show()

if __name__ == "__main__":
    main()
