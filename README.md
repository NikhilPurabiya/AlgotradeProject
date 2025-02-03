

# 📈 Simple Trading Algorithm with Python & Yahoo Finance  

### 🚀 An Automated Trading Strategy for SPY (S&P 500 ETF)  

This project implements a **basic algorithmic trading strategy** using **Python** and **Yahoo Finance** (`yfinance`). The strategy automatically **buys and sells SPY** based on a **10% price movement rule**, maintaining a trading record and visualizing results.  

## 📌 Features  

✔️ **Fetches Historical Stock Data** using `yfinance` 📊  
✔️ **Implements a Simple Trading Logic** (Buy & Sell based on 10% price movement)  
✔️ **Manages Portfolio** (Tracks Cash Balance, Trades, and Holdings) 💰  
✔️ **Visualizes Buy & Sell Points** using `matplotlib` 📈  

## ⚙️ Installation  

Ensure you have **Python 3.x** installed, then install the required dependencies:  

```sh
pip install pandas yfinance matplotlib
```

## 🛠️ How It Works  

1️⃣ **Data Collection**:  
   - Fetches historical stock data for **SPY** (S&P 500 ETF) from Yahoo Finance.  
   - Computes **daily returns**.  

2️⃣ **Trading Logic**:  
   - **Buy**: Enters a position when no shares are held.  
   - **Sell**: Exits the position if the stock price **increases or decreases by 10%**.  
   - Implements a **cool-down period of 31 days** between trades.  

3️⃣ **Results Visualization**:  
   - Plots the **stock price** with **buy & sell points** for clear strategy evaluation.  

## 📝 Code Structure  

- `SimpleTradingAlgorithm` (Class)  
  - `load_data()`: Fetches and processes stock data  
  - `run_strategy()`: Implements the trading logic  
  - `buy()`: Executes buy orders  
  - `sell()`: Executes sell orders  
  - `plot_results()`: Plots stock price with buy/sell signals  

- **Main Execution (`if __name__ == "__main__"`)**:  
  - Instantiates the algorithm, runs it, and displays final **cash balance & trading chart**.  

## 📊 Example Output  

```
Fetching data for SPY from 2020-01-01 to 2021-01-01
2020-01-02: BUY 385 shares at $259.81
2020-04-29: SELL 385 shares at $285.88
Final Cash: $110201.33
```

✅ **Trade execution and final cash balance are printed.**  
✅ **Chart showing buy & sell points is generated.**  

## 📌 Sample Visualization  

![Trading Strategy Plot](https://via.placeholder.com/800x400?text=Trading+Strategy+Visualization)  

## 🚀 Future Enhancements  

- **Optimize Entry & Exit Strategies** for better returns 📊  
- **Backtest with Different Stocks** (AAPL, TSLA, QQQ, etc.) 📈  
- **Implement Stop-Loss & Trailing Stop Mechanisms** 🚀  
- **Expand Strategy to Multi-Asset Portfolios** 💰  

## 🤝 Contributing  

Got suggestions or want to enhance the strategy? **Fork the repo**, create a branch, and submit a PR!  

## 📜 License  

This project is licensed under the MIT License.  
 🔗 Connect with Me  
GitHub: [Nikhil Purabiya](https://github.com/NikhilPurabiya)  
