import os
import joblib
import pandas as pd

# ==========================================================
# Load ML Model
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "demand_model.pkl"
)

try:

    model = joblib.load(MODEL_PATH)

    print("Demand Model Loaded Successfully")

except Exception as e:

    print("Error Loading Model")
    print(e)

    model = None


# ==========================================================
# Predict Demand
# ==========================================================

def predict_book_demand(

        book_id,
        month_no,
        total_issues,
        recent_issues,
        available_quantity

):

    if model is None:
        return 0

    data = pd.DataFrame({

        "book_id":[book_id],

        "month_no":[month_no],

        "total_issues":[total_issues],

        "recent_issues":[recent_issues],

        "available_quantity":[available_quantity]

    })

    prediction = model.predict(data)

    demand = int(round(prediction[0]))

    if demand < 0:
        demand = 0

    return demand


# ==========================================================
# Stock Recommendation
# ==========================================================

def recommend_purchase(

        predicted_demand,
        available_quantity

):

    purchase = max(0, predicted_demand - available_quantity)

    if purchase == 0:

        status = "Safe"

    elif purchase <= 10:

        status = "Medium"

    elif purchase <= 20:

        status = "Low Stock"

    else:

        status = "Critical"

    return {

        "status": status,

        "purchase": purchase

    }


# ==========================================================
# Confidence Score
# ==========================================================

def get_confidence(

        total_issues,
        recent_issues

):

    if total_issues == 0:

        return 70

    confidence = 80 + min(15, recent_issues)

    return confidence


# ==========================================================
# Complete Prediction
# ==========================================================

def predict_complete(

        book_id,
        month_no,
        total_issues,
        recent_issues,
        available_quantity

):

    demand = predict_book_demand(

        book_id,

        month_no,

        total_issues,

        recent_issues,

        available_quantity

    )

    purchase = recommend_purchase(

        demand,

        available_quantity

    )

    confidence = get_confidence(

        total_issues,

        recent_issues

    )

    return {

        "predicted_demand": demand,

        "status": purchase["status"],

        "purchase": purchase["purchase"],

        "confidence": confidence

    }


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    result = predict_complete(

        book_id=1,

        month_no=7,

        total_issues=150,

        recent_issues=35,

        available_quantity=12

    )

    print("=" * 60)

    print("AI BOOK DEMAND PREDICTION")

    print("=" * 60)

    print("Predicted Demand :", result["predicted_demand"])

    print("Stock Status     :", result["status"])

    print("Purchase Needed  :", result["purchase"])

    print("Confidence Score :", str(result["confidence"]) + "%")

    print("=" * 60)