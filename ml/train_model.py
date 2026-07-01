import pandas as pd
import pickle
import os

from flask import Flask
from flask_mysqldb import MySQL

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Flask Config

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "smart_library1"

mysql = MySQL(app)

#Create models folder

if not os.path.exists("models"):
    os.makedirs("models")

with app.app_context():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            book_id,
            book_name,
            author,
            category
        FROM books
    """)

    books = cursor.fetchall()

    cursor.close()
#DataFrame

df = pd.DataFrame(
books,
columns=[
"book_id",
"book_name",
"author",
"category"
]
)

#Handle Null Values

df["author"] = df["author"].fillna("")
df["category"] = df["category"].fillna("")

#Create Features

df["features"] = (
df["author"] + " " +
df["category"]
)

#Vectorization

cv = CountVectorizer()

matrix = cv.fit_transform(df["features"])

#Similarity Matrix

similarity = cosine_similarity(matrix)

#Save Files

pickle.dump(
similarity,
open("models/similarity.pkl", "wb")
)

pickle.dump(
df,
open("models/books_df.pkl", "wb")
)

pickle.dump(
cv,
open("models/vectorizer.pkl", "wb")
)

print("=" * 50)
print("Book Recommendation Model Trained Successfully")
print("Total Books :", len(df))
print("Models Saved Inside /models Folder")
print("=" * 50)

