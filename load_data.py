import pandas as pd

# Load MovieLens data (u.data and u.item files)
ratings_columns = ['userId', 'movieId', 'rating', 'timestamp']
ratings_data = pd.read_csv('data/u.data', sep='\t', names=ratings_columns)

movies_columns = ['movieId', 'title', 'releaseDate', 'videoReleaseDate', 'IMDbURL']
movies_data = pd.read_csv('data/u.item', sep='|', encoding='latin-1', names=movies_columns)

# Convert numpy.int64 to Python int to avoid issues with MongoDB
ratings_data['movieId'] = ratings_data['movieId'].astype(int)
movies_data['movieId'] = movies_data['movieId'].astype(int)

# Save as CSV files with the correct data types
ratings_data.to_csv('movie_ratings.csv', index=False)
movies_data[['movieId', 'title']].to_csv('movies.csv', index=False)

print("Files saved successfully with the correct data types.")

