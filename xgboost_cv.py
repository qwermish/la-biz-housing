import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
import matplotlib.pyplot as plt

df = pd.read_csv('all_biz_cult.csv')

df = df.rename(columns={'biz_count':'ind_art_count'})

def disc_val(price):
    for i in range(10):
        if price<100000*(i+1) and price>=100000*i:
            return i
        
df['discrete_val'] = df['value'].apply(disc_val)
print len(df)
df = df.dropna(subset = ['discrete_val'])
print len(df)

with open('business_types.txt') as f:
    feats = f.read().splitlines()
                                          
feats.append('ind_art_count') # of indep artists within 0.5 miles
feats.append('cult_count')

X = df[feats]
Y = df['discrete_val']
X_train, X_val, Y_train, Y_val = train_test_split(X, Y)

#CODE USED FOR CROSS-VALIDATION IS COMMENTED OUT FOR FINAL PREDICTION

## cv_params = {'max_depth': [3,5,7], 'min_child_weight': [1,3,5] }
## ind_params = {'learning_rate': 0.1, 'n_estimators': 1000, 'seed':0, 'subsample': 0.8, 
##              'objective': 'multi:softprob'}

## cv_params = {'learning_rate': [0.1, 0.01], 'subsample': [0.7,0.8,0.9]}
## ind_params = {'n_estimators': 1000, 'seed':0, 'colsample_bytree': 0.8, 
##              'objective': 'multi:softprob', 'max_depth': 3, 'min_child_weight': 5}   
    
## model = xgb.XGBClassifier(**ind_params)

## optimized_GBM = GridSearchCV(model, 
##                             cv_params, 
##                              scoring = 'neg_log_loss', cv = 5) 

## optimized_GBM.fit(X_train, Y_train)

#print optimized_GBM.grid_scores_

#optimal params: mean: -1.65716, std: 0.02265, params: {'max_depth': 3, 'min_child_weight': 5}
# with zip code added: mean: -1.49501, std: 0.02009, params: {'subsample': 0.8, 'learning_rate': 0.01}
#with zip code and area: mean: -1.25081, std: 0.03286, params: {'max_depth': 3, 'min_child_weight': 5}
# ditto, with above params: mean: -1.04992, std: 0.04376, params: {'subsample': 0.8, 'learning_rate': 0.01}

xgdmat = xgb.DMatrix(X_train, Y_train)

our_params = {'eta': 0.01, 'seed':0, 'subsample': 0.8, 'colsample_bytree': 0.8, 
             'objective': 'multi:softprob', 'max_depth':3, 'min_child_weight':5, 'num_class': 10} 

## cv_xgb = xgb.cv(params = our_params, dtrain = xgdmat, num_boost_round = 3000, nfold = 5,
##                 metrics = ['mlogloss'], # Make sure you enter metrics inside a list or you may encounter issues!
##                 early_stopping_rounds = 100) # Look for early stopping that minimizes error

## print cv_xgb.tail(5)
                    
final_gb = xgb.train(our_params, xgdmat, num_boost_round = 1461)
#1461 chosen from cv_xgb above

importances = final_gb.get_fscore()
print importances

plt.bar(range(5), sorted(importances.values())[:5], align='center')
plt.xticks(range(5), sorted(importances, key=importances.get)[:5], rotation=90)
plt.xlabel('Importances of features w.r.t. housing price')
plt.title('Top 5 least important businesses that affect nearby housing prices')
plt.tight_layout()
plt.savefig('5_;st_imp_biz.png')

plt.bar(range(5), sorted(importances.values())[-5:], align='center')
plt.xticks(range(5), [elem[:24] for elem in sorted(importances, key=importances.get)[-5:]], rotation=90)
plt.xlabel('Importances of features w.r.t. housing price')
plt.title('Top 5 most important businesses that affect nearby housing prices')
plt.tight_layout()
plt.savefig('5_most_imp_biz.png')

                
testdmat = xgb.DMatrix(X_val)
Y_test = final_gb.predict(testdmat)

print log_loss(Y_val, Y_test)

#log loss with floor area and zip code: 1.00480217919
#log loss with only business info: 1.45136371123
