import pandas as pd
import numpy as np

# Load the dataset
file_path = "Mock_Trading_Data.csv"  # Ensure the file is in the same directory or provide the correct path
df = pd.read_csv(file_path)

# Define trading parameters
VRP_THRESHOLD = 5  # Minimum volatility risk premium required to enter a trade
INITIAL_CAPITAL = 10000  # Starting portfolio capital
TRADE_SIZE = 100  # Number of units per trade
NUM_TRADES = 50  # Number of random trades to simulate

# Randomly sample data to simulate different trade entries
sampled_data = df.sample(n=NUM_TRADES, replace=True, random_state=np.random.randint(0, 10000))

# Simulate trading strategy
capital = INITIAL_CAPITAL
trade_results = []

for _, row in sampled_data.iterrows():
    if row["vrp"] > VRP_THRESHOLD:  # Enter trade when IV > RV by threshold
        entry_price = row["market_price"]
        exit_price = entry_price * (1 + np.random.uniform(-0.02, 0.02))  # Simulated exit price variation
        pnl = (exit_price - entry_price) * TRADE_SIZE  # Profit/loss for the trade
        capital += pnl
        trade_results.append(pnl)

# Calculate performance metrics
if trade_results:
    sharpe_ratio = np.mean(trade_results) / np.std(trade_results) if np.std(trade_results) != 0 else 0
    max_drawdown = np.min(np.cumsum(trade_results))
    profit_loss_ratio = np.sum(np.array(trade_results) > 0) / max(1, np.sum(np.array(trade_results) < 0))
else:
    sharpe_ratio, max_drawdown, profit_loss_ratio = 0, 0, 0

# Output results
print("Performance Summary")
print("-------------------")
print(f"Final Capital: ${capital:.2f}")
print(f"Total Trades: {len(trade_results)}")
print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
print(f"Max Drawdown: ${max_drawdown:.2f}")
print(f"Profit/Loss Ratio: {profit_loss_ratio:.2f}")
