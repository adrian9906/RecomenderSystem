
from pandas import DataFrame
import pandas as pd
def mean_df(data: DataFrame):
    meandata = []
    dataMean = data.groupby('movie_title').agg(avg_rating = ('rating', 'mean'),
                                                number_of_ratings = ('rating', 'count')).reset_index()
    avg_ratings100 = dataMean[dataMean['number_of_ratings']>100]
    
    sortedData = sorted(avg_ratings100.values.tolist(), key=lambda x: x[1],reverse=True)
    
    for movie in sortedData:
        dict = {
            'movie': movie[0],
            'rating': movie[1]
        }
        meandata.append(dict)
    
    
    return meandata