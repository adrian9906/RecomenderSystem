import json
import pandas as pd  
from .mean import mean_df

def process_Data(data:dict, item:dict):
    dfData = pd.DataFrame(data)  
    dfItem = pd.DataFrame(item)
    
    dfMerge_Data_Item = pd.merge(dfData,dfItem, how='inner',left_on='item_id', right_on='id')
    
    merged_df_ratings = mean_df(dfMerge_Data_Item)
    
    # Make the user matrix and movies
    movies_ratings_pivot = pd.pivot_table(merged_df_ratings, index='user_id', columns='movie_title', values='rating', fill_value = 0)

    