import json
from fastapi import FastAPI, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
from Pre_Process.mean import mean_df

from Pre_Process.processingDataset import averageData, process_Data

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

@app.get("/recommend")
def recommendMovies():
    with open('./data.json',mode = 'r') as file:
        data = json.load(file)  
    with open('./item.json',mode = 'r') as file:
        item = json.load(file)
    dfMerge_Data_Item = process_Data(data,item)
    meanData = mean_df(dfMerge_Data_Item)
    
    return {'Recommend_Movies': meanData}
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
    
    