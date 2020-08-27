# Import libraries here
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


def con(x):
    try:
        return(float(x.split('/')[0]))
    except:
        return(0.0)#missing value
def con2(x):
    try:
        x = x.split(',')
        if len(x) > 1:
            return(float(x[0]+x[1]))
        else:
            return(float(x[0]))
    except:
        return(0.0)

#used for free text matching
def find_f_score(free_text, row):
    c = 0.0;
    l = len(free_text.split(' '))
    try:
        for token in free_text.split(' '):
            if (token.lower() in row['dish_liked'].lower()):
                c = c+1
            elif token.lower() in row['reviews_list'].lower():
                c = c+1
            elif token.lower() in row['menu_item'].lower():
                c = c+1
            elif token.lower() in row['rest_type'].lower():
                c = c+1
        #print(c,l,c/l)
        return(c/l)
    except:
        return(c/l)
    
def find_top_recomendation(df, location, cost, cuisine, free_text, top, max_votes):
    ##loop through all the shops
    dic = {'shop_id': [], 'f_score':[], 't_score':[],'loc':[],'cos':[],'csin':[],'n_rating':[],          'n_votes':[]}
    for index, row in df.iterrows():
        loc = 0;
        cos = 0;
        csin  = 0;
        f_score = 0;
        t_score = 0;
        n_rating = 0;
        n_votes = 0;
        if location == row['location']:#filter condiction 1
            loc = 1;
        if row['cost'] <= cost:#filter condiction 2
            cos = 1;
        if cuisine.lower() in row['cuisines'].lower():#filter condiction 3
            csin = 1;
        f_score = find_f_score(free_text, row)##free test matching score
        
        #save in dic
        dic['shop_id'].append(row['shop_id'])
        dic['f_score'].append(f_score)
        dic['loc'].append(loc)
        dic['cos'].append(cos)
        dic['csin'].append(csin)
        
        n_rating = row['rating']/5
        dic['n_rating'].append(n_rating)
        
        n_votes  = row['votes']/max_votes
        dic['n_votes'].append(n_votes)
        
        #total score = location match [0/1] + within budget [0/1] + free text score 
                        #+ normalized rating + normalized votes
        t_score = loc + cos + csin + f_score + n_rating + n_votes
        
        dic['t_score'].append(t_score) ##final score after adding all the score
    
    dic = pd.DataFrame(dic)#create df
    
    return(dic.nlargest(top, 't_score'))##select top recomendation


# read data
print("start loading data====")
df = pd.read_csv('../data/training/training-RestoInfo.zip')
#rename Unnamed: 0 collumn to shop_id
df.rename(columns={'Unnamed: 0':'shop_id'}, inplace=True)
print("Loading data done====\n")
print(df.head())

#basic preporossing
col_name = 'rate'
df['rating'] = df['rate'].apply(lambda x: con(x))

## approx_cost(for two people)
col_name = 'approx_cost(for two people)'
df['cost'] = df[col_name].apply(lambda x: con2(x))


## input test case 1

location = 'Koramangala'
cost = 500
cuisine = 'North Indian'
free_text = 'good ambiance restaurants, serving fish'
top = 3
max_votes = df['votes'].max()
top3 = find_top_recomendation(df, location, cost, cuisine, free_text, top, max_votes)
print(f"Search location: {location}\n")
print(f"Buget: {cost}\n")
print(f"Cuisine: {cuisine}\n")
print(f"Free text: {free_text}\n")
print(f"Top {top} recomended shops = ",top3[['shop_id','t_score']])
##t_score = agregated score of all the important factors 

