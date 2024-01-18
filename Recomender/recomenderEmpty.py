
from pandas import DataFrame
from Pre_Process.mean import mean_df



def recomendFirtsMovies(data:DataFrame):
    recomend_movies = mean_df(data)
    
    return recomend_movies