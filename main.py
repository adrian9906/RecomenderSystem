import json
from fastapi import FastAPI, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError

from Pre_Process.mean import mean_df

from Pre_Process.processingDataset import averageData, get_pivot, process_Data
from Pre_Process.similarity import cosein_similarity_movies, similarity_data
from Recomender.similarMovies import similarMovies_notWatched, watchedMovies
from Recomender.similarUsers import similar_users_movies
from Recomender.topSimilarUsers import top_similar_users
from db.CRUD.Find import FindOne, findDoc
from logger.exception_handlers import request_validation_exception_handler, http_exception_handler, unhandled_exception_handler
from logger.middleware import log_request_middleware
from logger.log_config import log_config

app = FastAPI()

origins = [
    "*"
]

app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

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
    data = findDoc('RecomenderDataset','UserMovieData')
    item = findDoc('RecomenderDataset','MovieData')
    dfMerge_Data_Item = process_Data(data,item)
    meanData = mean_df(dfMerge_Data_Item)
    
    return {'Recommend_Movies': meanData}
    
@app.get("/recommend/similarUsers")
def getSimilarUsers(id: int):
    data = findDoc('RecomenderDataset','UserMovieData')
    item = findDoc('RecomenderDataset','MovieData')
    if FindOne('RecomenderDataset','UserMovieData',query={'user_id':id}):
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

@app.get("/recommend/moviesNotWatched")
def getSimilarMovies(id: int):
    data = findDoc('RecomenderDataset','UserMovieData')
    item = findDoc('RecomenderDataset','MovieData')
    if FindOne('RecomenderDataset','UserMovieData',query={'user_id':id}):
        dfMerge_Data_Item = process_Data(data,item)
        average = averageData(dfMerge_Data_Item)
        pivot = get_pivot(dfMerge_Data_Item, average)
        similarityDf = cosein_similarity_movies(pivot)
        similarMovies = similarMovies_notWatched(id,similarityDf,average,pivot)
        if similarMovies:
            return {f"Recommend movies to user {id}": similarMovies}
        else:
            return {f"Not similar movies found for user {id}"}
    
    else:
        return {"User not found in database"}

@app.get("/recommend/WatchedMovies")
def getWatchedMovies(id: int,n:int):
    data = findDoc('RecomenderDataset','UserMovieData')
    item = findDoc('RecomenderDataset','MovieData')
    if FindOne('RecomenderDataset','UserMovieData',query={'user_id':id}):
        dfMerge_Data_Item = process_Data(data,item)
        average = averageData(dfMerge_Data_Item)
        pivot = get_pivot(dfMerge_Data_Item, average)
        watched_movies = watchedMovies(id,pivot,n)
        
        if watched_movies:
            return {f"Watched movies by user {id} are": watched_movies}
        else:
            return {f"Not watched any movies"}
    
    else:
        return {"User not found in database"}


@app.get("/recommend/usersMostSimilars")
def get_similarUsers(id: int,n:int):
    data = findDoc('RecomenderDataset','UserMovieData')
    item = findDoc('RecomenderDataset','MovieData')
    if FindOne('RecomenderDataset','UserMovieData',query={'user_id':id}):
        dfMerge_Data_Item = process_Data(data,item)
        average = averageData(dfMerge_Data_Item)
        pivot = get_pivot(dfMerge_Data_Item, average)
        similarityDf = cosein_similarity_movies(pivot)
        similarUsers = top_similar_users(similarityDf,id,n=10,threshold=0.6)
        if similarUsers:
            return {f"The most similar users to user {id} are": similarUsers}
        else:
            return {f"Not similar users found for user {id}"}
    
    else:
        return {"User not found in database"}
if __name__ == "__main__":
    uvicorn.run("main:app",reload='--reload-include', host="127.0.0.1", port=8000, log_level="info")
    
    