# This is for building database model from local, so there must be three csv files named pop_song.csv,lyrics.csv and itunes.csv in the working directory!
# The output is a db file with three Tables.

import pandas as pd
import sqlite3
def csv_to_db():
    conn= sqlite3.connect("pop_music_local.db")
    df_popsong = pd.read_csv('pop_song.csv')
    df_popsong.to_sql('Pop_Song', conn, if_exists='append', index=False)
    df_lyrics = pd.read_csv('lyrics.csv')
    df_lyrics.to_sql('Lyrics', conn, if_exists='append', index=False)
    df_itunes = pd.read_csv('itunes.csv')
    df_itunes.to_sql('Collection', conn, if_exists='append', index=False)
    conn.commit() 
    conn.close()
    print('csv files successfully stored into db!')