import os
import pandas as pd 

df = pd.read_csv('output.csv')
for i, r in df.iterrows():
    movie_name = r['movie_name']
    print(movie_name)
    file = r['file_name']

    if(os.path.isfile(file)):
        with open('exits.txt','a') as f:
            f.write(movie_name+'\n')
    else:
        with open('not_exits.txt', 'a') as f1:
            f1.write(movie_name+'\n')
