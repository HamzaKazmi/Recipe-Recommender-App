from surprise import SVD
import pandas as pd
from surprise import Dataset
from surprise import Reader
from collections import defaultdict
from surprise.model_selection import cross_validate
import databaseCon

con = databaseCon.Database()
loadedData = con.selectAll()

userGroupId = loadedData[0]
ingredientId = loadedData[1]
ratings = loadedData[2]

#Train and get recommendations for a user using SVD algorthm
def do_Predict():
    ratings_dict = {'userID': userGroupId,
                    'itemID': ingredientId,
                    'rating': ratings}

    df = pd.DataFrame(ratings_dict)
    reader = Reader(rating_scale=(1, 4))
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)
    testset = trainset.build_anti_testset()
    predictions = algo.test(testset)
    cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    return get_top_n(predictions)

#Get top n recommendations for a user
def get_top_n(predictions, n = 20):
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

#return recommended items
def getRecommendedItems(uid):
    recommendations = do_Predict()
    for users in recommendations.items():
        if users[0] == uid:
            return(users[1])


