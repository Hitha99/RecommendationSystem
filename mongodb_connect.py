from pymongo import MongoClient
import pandas as pd

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['movie_recommendation']
users_collection = db['users']
movies_collection = db['movies']
ratings_collection = db['ratings']

# Load data from CSV
ratings = pd.read_csv('movie_ratings.csv')
movies = pd.read_csv('movies.csv')

# Insert data into MongoDB collections
for index, row in movies.iterrows():
    movies_collection.update_one(
        {'movieId': row['movieId']},
        {'$set': {'title': row['title']}},
        upsert=True
    )

for index, row in ratings.iterrows():
    ratings_collection.update_one(
        {'userId': row['userId'], 'movieId': row['movieId']},
        {'$set': {'rating': row['rating']}},
        upsert=True
    )
