import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv(
    "ml/datasets/borrowing_history.csv"
)

X = data[[
    "days_issued",
    "member_age",
    "books_taken"
]]

y = data["late_return"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

with open(
    "ml/trained_models/late_return.pkl",
    "wb"
) as f:

    pickle.dump(model, f)

print("Late Return Prediction Model Trained")