# final conclusions

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

# When there is just one track in a collection, the song's a single. There are singles and non-singles in the 
# ranking list. Often, when a singer release a new song as a single, we may think of it as an emphasis which means 
# this song has higher quality and fans shouldn't miss it! Is this really the case? 
# To answer the question, this project is interested in exploring the difference of quality and price bewtween singles and non-single songs. 
# To quantify, the solution will try to break through on their difference in terms of price_per_song and rankings.

def conclusions(db_file):
    # conclusion1: ranking and price line graph
        # non-single songs
    conn = sqlite3.connect(db_file)
    query_rp_n = '''SELECT DISTINCT p.name as song_name,p.ranking as ranking,c.mean_price_each_song as price
               FROM Pop_Song p JOIN Collection c ON p.ranking=c.song_id
               WHERE c.track_count>1'''
    df_rp_n = pd.read_sql(query_rp_n, conn)
    pic = df_rp_n.plot(x='ranking',y='price',label='non-single songs')

        # single songs
    query_rp_s = '''SELECT DISTINCT p.name as song_name,p.ranking as ranking,c.mean_price_each_song as price
               FROM Pop_Song p JOIN Collection c ON p.ranking=c.song_id
               WHERE c.track_count=1'''
    df_r_s = pd.read_sql(query_rp_s, conn)
    df_r_s.plot(x='ranking',y='price',label='single songs',ax=pic)
    plt.show()#line plot

   
    # conclusion2: difference in mean ranking and price - bar plots
        # single songs
    query_single = '''SELECT DISTINCT p.name as song_name,p.ranking as ranking,c.mean_price_each_song 
           FROM Pop_Song p JOIN Collection c ON p.ranking=c.song_id
           WHERE c.track_count=1'''

    df_single = pd.read_sql(query_single, conn)
    single_mean_price = df_single['mean_price_each_song'].mean()
    single_mean_ranking =  df_single['ranking'].mean()
        # non-single songs
    query_nonsingle = '''SELECT DISTINCT p.name as song_name,p.ranking as ranking,c.mean_price_each_song 
               FROM Pop_Song p JOIN Collection c ON p.ranking=c.song_id
               WHERE c.track_count>1'''
    df_nonsingle = pd.read_sql(query_nonsingle, conn)
    nonsingle_mean_price =df_nonsingle['mean_price_each_song'].mean()
    nonsingle_mean_ranking =df_nonsingle['ranking'].mean()

    print('Single: price: '+str(single_mean_price)+' '+'ranking: '+str(single_mean_ranking))
    print('Nonsingle: price: '+str(nonsingle_mean_price)+' '+'ranking: '+str(nonsingle_mean_ranking))

    x1 = ['single','non-single']
    y1 = [single_mean_price,nonsingle_mean_price]
    plt.bar(x1, y1,width=0.5)
    plt.title("Price Difference")
    plt.xlabel("song_mean_price")
    plt.ylabel("dollar")
    plt.show() 

    x2 = ['single','non-single']
    y2 = [single_mean_ranking,nonsingle_mean_ranking]
    plt.bar(x2, y2,width=0.5,color='orange')
    plt.title("Ranking Difference")
    plt.xlabel("song_mean_ranking")
    plt.ylabel("No.")
    plt.show() 