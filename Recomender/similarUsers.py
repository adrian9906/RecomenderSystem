

import pandas as pd
from pandas import DataFrame


def similar_users_movies(top_similar_usersList:list,movies_ratings_pivot:pd.DataFrame):  
    movies_result = []
    
    for user in top_similar_usersList:
        watched_movies = movies_ratings_pivot.loc[movies_ratings_pivot.index == user, movies_ratings_pivot.loc[user,:]>0]
        movieName = pd.DataFrame(watched_movies).columns.to_list()
        rating = pd.DataFrame(watched_movies).values.tolist()[0]
        movieList = sorted(list(zip(movieName,rating)),key= lambda x: x[1])
        dict = {
            'similar_user':user,
            'movies': movieList
            }
        movies_result.append(dict)
        
    return movies_result