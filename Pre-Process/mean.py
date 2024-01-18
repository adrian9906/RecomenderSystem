
from pandas import DataFrame
import pandas as pd
def mean_df(data: DataFrame):
    dataMean = data.groupby('movie_title').agg(avg_rating = ('rating', 'mean'),
                                                number_of_ratings = ('rating', 'count')).reset_index()
    avg_ratings100 = dataMean[dataMean['number_of_ratings']>100]

    merged_df = pd.merge(data, avg_ratings100[['movie_title']], on='movie_title', how='inner')
    
    return merged_df