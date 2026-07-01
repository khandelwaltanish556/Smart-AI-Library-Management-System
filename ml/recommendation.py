import pickle

similarity = pickle.load(
open("models/similarity.pkl", "rb")
)

df = pickle.load(
open("models/books_df.pkl", "rb")
)

def recommend_books(book_name):

    if book_name not in df["book_name"].values:
        return []

    index = df[df["book_name"] == book_name].index[0]

    scores = list(enumerate(similarity[index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for item in scores[1:7]:

        recommendations.append({
            "book_id": int(df.iloc[item[0]]["book_id"]),
            "book_name": df.iloc[item[0]]["book_name"],
            "author": df.iloc[item[0]]["author"],
            "category": df.iloc[item[0]]["category"]
        })

    return recommendations

if __name__ == "__main__":

    result = recommend_books("Python Programming")

    print("\nRecommended Books:\n")

    for book in result:

        print(book)