import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

print("\n🤖 Running Finance Prediction Model...\n")

df = pd.read_csv("data/transactions.csv")

df["Date"] = pd.to_datetime(df["Date"])

# Convert date to numeric feature
df["Day"] = df["Date"].dt.day

# Only expense data
expense_df = df[df["Type"] == "Expense"]

X = expense_df[["Day"]]
y = expense_df["Amount"]

model = LinearRegression()
model.fit(X, y)

# Predict next days
future_days = np.array([[31], [32], [33], [34], [35]])
predictions = model.predict(future_days)

print("📊 Future Expense Prediction:\n")

for day, pred in zip(future_days, predictions):
    print(f"Day {day[0]} → Expense: {round(pred,2)}")