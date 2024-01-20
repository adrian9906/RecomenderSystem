

def top_similar_users(similarityDf,select_userid,n=10,threshold=0.7):
    top_similar_users = similarityDf[similarityDf[select_userid]>threshold][select_userid].drop[select_userid].sort_values(ascending=False)[:n]
    top_similar_usersList = top_similar_users.index.to_list()
    
    return top_similar_usersList