

from pandas import DataFrame
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def cosein_similarity_movies(data:DataFrame):
    similarity_matrix = cosine_similarity(data)
    similarity_matrix_df = pd.DataFrame(similarity_matrix, index=data.index, columns=data.index)
    
    return similarity_matrix_df
