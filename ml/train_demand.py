import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestRegressor

print("=" * 60)
print("BOOK DEMAND PREDICTION MODEL TRAINING")
print("=" * 60)

# ==========================================
# CSV PATH
# ==========================================

csv_file = r"../issued_books/issue_books.csv"

if not os.path.exists(csv_file):
    print("CSV File Not Found!")
    exit()

# ==========================================
# READ DATASET
# ==========================================

df = pd.read_csv(csv_file)

print("Dataset Loaded Successfully")
print("Total Records :", len(df))

# ==========================================
# Convert Dates
# ==========================================

df["issue_date"] = pd.to_datetime(df["issue_date"])
df["due_date"] = pd.to_datetime(df["due_date"])

# Current Month
df["month_no"] = df["issue_date"].dt.month

# ==========================================
# Create Features
# ==========================================

issue_count = df.groupby("book_id").size().reset_index(name="total_issues")

recent_issue = (
    df.groupby("book_id")
    .tail(30)
    .groupby("book_id")
    .size()
    .reset_index(name="recent_issues")
)

feature_df = issue_count.merge(
    recent_issue,
    on="book_id",
    how="left"
)

feature_df["recent_issues"] = feature_df["recent_issues"].fillna(0)

feature_df["month_no"] = df["month_no"].max()

feature_df["available_quantity"] = 10

# ==========================================
# Target
# ==========================================

feature_df["next_month_demand"] = (
    feature_df["total_issues"] * 0.8 +
    feature_df["recent_issues"] * 0.2
)

# ==========================================
# Features
# ==========================================

X = feature_df[
    [
        "book_id",
        "month_no",
        "total_issues",
        "recent_issues",
        "available_quantity"
    ]
]

y = feature_df["next_month_demand"]

# ==========================================
# Train Model
# ==========================================

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X, y)

# ==========================================
# Save Model
# ==========================================

os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/demand_model.pkl"
)

feature_df.to_csv(
    "models/book_features.csv",
    index=False
)

print("=" * 60)
print("Model Trained Successfully")
print("Training Records :", len(feature_df))
print("Model Saved : models/demand_model.pkl")
print("Features Saved : models/book_features.csv")
print("=" * 60)