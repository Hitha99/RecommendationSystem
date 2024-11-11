from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import redis
from flask import Flask, jsonify, request

# Retrieve ratings data from MongoDB
ratings_data = pd.DataFrame(list(ratings_collection.find()))
movie_data = pd.DataFrame(list(movies_collection.find()))

# Create a user-item matrix (pivot table)
ratings_matrix = ratings_data.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

# Compute the cosine similarity between movies
cosine_sim = cosine_similarity(ratings_matrix.T)  # Similarity between items (movies)
cosine_sim_df = pd.DataFrame(cosine_sim, index=ratings_matrix.columns, columns=ratings_matrix.columns)

def get_movie_recommendations(movie_id, top_n=5):
    """ Get top N movie recommendations based on cosine similarity """
    similar_movies = cosine_sim_df[movie_id].sort_values(ascending=False)[1:top_n+1]
    recommended_movie_ids = similar_movies.index
    recommended_movies = movie_data[movie_data['movieId'].isin(recommended_movie_ids)]
    return recommended_movies[['movieId', 'title']]

# Set up Redis connection
cache = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_recommendations(movie_id, recommendations):
    """ Cache movie recommendations in Redis """
    cache.set(movie_id, recommendations.to_json(orient='records'))

def get_cached_recommendations(movie_id):
    """ Retrieve movie recommendations from Redis cache """
    cached_recommendations = cache.get(movie_id)
    if cached_recommendations:
        return pd.read_json(cached_recommendations)
    return None


app = Flask(__name__)

@app.route('/recommendations', methods=['GET'])
def recommend_movies():
    movie_id = int(request.args.get('movie_id'))  # Movie ID input from URL query params
    cached_recs = get_cached_recommendations(movie_id)

    if cached_recs is not None:
        return jsonify(cached_recs.to_dict(orient='records')), 200
    else:
        recommendations = get_movie_recommendations(movie_id)
        cache_recommendations(movie_id, recommendations)
        return jsonify(recommendations.to_dict(orient='records')), 200

if __name__ == "__main__":
    app.run(debug=True)
