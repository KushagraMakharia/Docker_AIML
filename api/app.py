from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd
import sklearn
import os
from pymongo import MongoClient
import numpy as np


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to your MongoDB database
connection_string = os.environ['ENV_MongoConnectionString']
client = MongoClient(connection_string)
db = client['CineManch']
collection = db['users']


# get available movies name
@app.route('/get_movies', methods=['GET'])
@cross_origin()
def get_movies():
    df = pd.read_csv("./artifacts/movie_idx.csv")
    movies = df["title"].to_list()
    return jsonify({'title': movies})


# Create a new document
@app.route('/save_entry', methods=['POST'])
@cross_origin()
def create_item():
    data = request.json
    df = pd.read_csv("./artifacts/movie_idx.csv")
    title = data["title"]
    movieId = df[df.title == title]["id"].item()
    entry = {"userId":str(data["userId"]), "movieId": movieId, "viewed": 1}
    item_id = collection.insert_one(entry).inserted_id
    return jsonify({'message': 'Item created', 'item_id': str(item_id)})


# get prediction
@app.route('/get_recommendations', methods=['POST'])
@cross_origin()
def get_recommendations():
    data = request.json
    title = data["title"]
    df = pd.read_csv("./artifacts/movie_idx.csv")
    user_df = pd.read_csv("./artifacts/user_data.csv")
    # Content based recommendations
    cosine_sim = pickle.load(open("./artifacts/cosine_matrix.pkl", 'rb'))
    idx =  df.index[df.title == title][0]
    movieId = df[df.title == title]["id"].values[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    cbr_recc = df["title"].iloc[movie_indices].to_list()

    # Collaborating Filtering Recc.
    userMoviesId = list(set(user_df['movieId'].tolist()))
    collab_recc = []
    if movieId in userMoviesId:     
        vh = pickle.load(open("./artifacts/svd_matrix.pkl", 'rb'))   
        movie_userIdx = userMoviesId.index(movieId)
        temp = get_similar_recommendation(vh, movie_userIdx)
        collab_recc = get_movies(userMoviesId, temp, df)
    
    recc = list(set(collab_recc + cbr_recc))

    return jsonify({'movies': recc})

def cosine_similarity(v,u):
    return (v @ u)/ (np.linalg.norm(v) * np.linalg.norm(u))

def get_similar_recommendation(vh, movieIdx):
    res = []
    a = vh[:, movieIdx]
    for i in range(1, vh.shape[1]):
        if i == movieIdx:
            continue
        else:
            b = vh[:, i]
            similarity = cosine_similarity(a, b)
            if abs(similarity) > 0.6:
                res.append(i)
    return res

def get_movies(moviesIds, idxs, df):
    moviesId = [moviesIds[x] for x in idxs]
    data = df[df.id.isin(moviesId)].title.tolist()
    return data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)