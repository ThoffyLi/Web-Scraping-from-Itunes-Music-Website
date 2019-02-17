# main program
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import requests
from bs4 import BeautifulSoup as BS
import bs4
import json

from web_to_csv import web_to_csv
from csv_to_db import csv_to_db
from web_to_db import web_to_db
from top_single import top_single
from conclusions import conclusions

scrap_url = 'http://www.popvortex.com/music/charts/top-pop-songs.php'
api_lyrics_endpoint = 'https://api.lyrics.ovh/v1/'
api_itunes_endpoint = 'https://itunes.apple.com/search?term='


def main():
    while True:
        # Allow user to get csv files to local, which enabling the later 'local' choice to work
        local_file=input("Do you want to acquire csv files from web first? input 'Y' or 'N':")
        if local_file!='Y' and local_file!='N':
            print("Invalid choice!\n")
            continue
        elif local_file=='Y':
            web_to_csv(scrap_url,api_lyrics_endpoint,api_itunes_endpoint)
            #for itunes api, if the information cannot be found within the api, the track_count will be set as minus(-1 or -2) and average_price_of_each_song is 0
            break
        else:
            print('\n')
            break


    while True:
        # Choose: build data model from remote or local
        remote_or_local = input('Please choose how to build data model! input "remote" or "local":')
        if remote_or_local!="remote" and remote_or_local!="local":
            print("Invalid choice!\n")
            continue
        elif remote_or_local=="remote":
            #From remote choice: get data from web scraping/api and directly build data model.
            print('Building data model from remote source, please wait.......')
            web_to_db(scrap_url,api_lyrics_endpoint,api_itunes_endpoint)
            db_name ='pop_music_remote.db'
            break
        else:
            #From local storage choice:store the csv files to database;
            #To do this, there must be three csv files named 'pop_song.csv','lyrics.csv' and 'itunes.csv' in the working directory! These files can be acquired b
            print('Building data model from local source, please wait.......')
            try:
                csv_to_db()
                db_name ='pop_music_local.db'
            except:
                print("csv files not found! Automatically choosing remote method!")
                print('Building data model from remote source, please wait.......')
                web_to_db(scrap_url,api_lyrics_endpoint,api_itunes_endpoint)
                db_name ='pop_music_remote.db'
            break
    print("\n")
    #display one result for hw5 : show the information and lyrics of the best single(only one track in a collection)
    while True:
        con_1 = input("Show the information and lyrics of the best single song? Y/N: ")
        if con_1!='Y' and con_1!='N':
            print("Invalid choice!\n")
            print('\n')
            continue
        elif con_1=='Y':
            top_single(db_name)
            print("\n")
            break
        else:
            break

    #display final conclusion
    while True:
        con_2 = input("Show the final conclusions? Y/N: ")
        if con_2!='Y' and con_2!='N':
            print("Invalid choice!\n")
            print('\n')
            continue
        elif con_2=='Y':
            conclusions(db_name)
            print("\n")
            break
        else:
            break

if __name__ =='__main__':
    main()

