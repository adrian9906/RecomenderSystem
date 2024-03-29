

import numpy as np
import pandas as pd


def similarMovies_notWatched(user,similaritydf:pd.DataFrame,avg_ratings100:pd.DataFrame,movies_ratings_pivot:pd.DataFrame):
    similarities = similaritydf[user].drop(user)
    
    weights = similarities/similarities.sum()
    
    not_watched_movies = movies_ratings_pivot.loc[movies_ratings_pivot.index != user, movies_ratings_pivot.loc[user,:]== 0]

    weighted_averages = pd.DataFrame(not_watched_movies.T.dot(weights.to_numpy()), columns=["weighted_avg"])
    
    weighted_averages_sorted = weighted_averages.sort_values(by='weighted_avg', ascending=False).head(20)
    
    weighted_averages_list = weighted_averages_sorted.index.tolist()
    
    not_watched_recommend = []
    for movie in weighted_averages_list:
        rating = round(avg_ratings100.loc[avg_ratings100["movie_title"] == movie,'avg_rating'].iloc[0],2)
        dict = {
            'movie':movie,
            'rating': rating
            }
        not_watched_recommend.append(dict)
    not_watched_recommend = sorted(not_watched_recommend,key=lambda x: x['rating'],reverse = True)
    return not_watched_recommend

def watchedMovies(user_id:int,movies_ratings_pivot:pd.DataFrame,n):
    watched_movies = movies_ratings_pivot.loc[movies_ratings_pivot.index == user_id, movies_ratings_pivot.loc[user_id,:]>0]
    movies = pd.DataFrame(watched_movies).columns.to_list()
    ratings = pd.DataFrame(watched_movies).values.tolist()[0]
    movies_dict = {movie: rating for movie , rating in zip(movies,ratings)}
    movies_dict_sorted = sorted(movies_dict.items(),key= lambda x: x[1],reverse=True)
    watched_movies_dict = {'user': user_id,'movies':movies_dict_sorted[:n]}
    return watched_movies_dict