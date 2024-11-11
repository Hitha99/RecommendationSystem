movie_recommendation/
│
├── app.py                # Flask API for recommendations
├── movie_ratings.csv     # User ratings dataset (generated from u.data)
├── movies.csv            # Movies metadata dataset (generated from u.item)
├── requirements.txt      # Dependencies

run pip install -r requirements.txt to get the tools.

Running the Application
------------------------------
Ensure MongoDB and Redis are running on your local machine.
Run the preprocessing script to convert and load the MovieLens dataset into MongoDB.
Run the Flask API:
python app.py

Access the API endpoint:
http://localhost:5000/recommendations?movie_id=1

This will return the top 5 movie recommendations based on movie ID 1.
