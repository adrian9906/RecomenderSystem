import json
from fastapi import FastAPI, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
from Pre_Process.mean import mean_df

from Pre_Process.processingDataset import averageData, get_pivot, process_Data
from Pre_Process.similarity import cosein_similarity_movies, similarity_data
from Recomender.similarUsers import similar_users_movies
from Recomender.topSimilarUsers import top_similar_users
from db.CRUD.Find import FindOne, findDoc

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET Methods

@app.get("/recommend")
def recommendMovies():
    data = findDoc('RecomenderSystem','UserMovieData')
    item = findDoc('RecomenderSystem','MovieData')
    dfMerge_Data_Item = process_Data(data,item)
    meanData = mean_df(dfMerge_Data_Item)
    
    return {'Recommend_Movies': meanData}
    
@app.get("/recommend/similarUsers")
def getSimilarUsers(id: int):
    data = findDoc('RecomenderSystem','UserMovieData')
    item = findDoc('RecomenderSystem','MovieData')
    if FindOne('RecomenderSystem','UserMovieData',query={'user_id':id}):
        dfMerge_Data_Item = process_Data(data,item)
        average = averageData(dfMerge_Data_Item)
        pivot = get_pivot(dfMerge_Data_Item, average)
        similarityDf = cosein_similarity_movies(pivot)
        similarUsers = top_similar_users(similarityDf,id,n=10,threshold=0.6)
        similarMovies = similar_users_movies(similarUsers, pivot)
        if similarMovies:
            return {f"Similar movies for user {id}": similarMovies}
        else:
            return {f"Not similar movies found for user {id}"}
    
    else:
        return {"User not found in database"}

if __name__ == "__main__":
    uvicorn.run("main:app",reload='--reload-include', host="127.0.0.1", port=8000, log_level="info")
    
    