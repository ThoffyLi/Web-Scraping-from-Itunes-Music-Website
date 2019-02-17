# This function is for building data model directly from web data(remote, no local files like csv,txt are created)
# The input are scraping url and api endpoints, the output is the database with three tables filled with data.

import requests
from bs4 import BeautifulSoup as BS
import bs4
import json
import sqlite3

def web_to_db(web_url,api_lyrics_endpt,api_itunes_endpt):
    def getr(u):
        try:
            r = requests.get(u,timeout=30)
            r.raise_for_status()
        except:
            print("error")
        return r
    
    # scrape web data
    r_scrape = getr(web_url)
    soup = BS(r_scrape.content,'lxml')
    main_table = soup.findAll('div',{'class':'chart-content col-xs-12 col-sm-8'})#for general information of a song
    song_list =[] 
    ranking = 1
    for s in main_table:
        song = dict()
        song['ranking']=ranking
        if len(s.find('a').text.split(','))>1:
            song['name'] = ''
            for n in s.find('a').text.split(','):
                song['name'] =song['name']+n+' '
        else:
            song['name'] = s.find('a').text
        
        if len(s.find('em').text.split(','))>1:
            song['artist']=''
            for a in s.find('em').text.split(','):
                song['artist'] =song['artist']+a+'&'
        else:
            song['artist']=s.find('em').text
        if s.findAll('li')[1].text[0] !='R':
            song['release_date']=s.findAll('li')[2].text.split(':')[1].split(',')[0]+s.findAll('li')[2].text.split(':')[1].split(',')[1]
            song['new release or not']='New'
        else:
            song['release_date']=s.findAll('li')[1].text.split(':')[1].split(',')[0]+s.findAll('li')[1].text.split(':')[1].split(',')[1]
            song['new release or not']='Not New'        
        song_list.append(song)
        ranking=ranking+1  
        
    # create Tables
    conn = sqlite3.connect('pop_music_remote.db')
    cur=conn.cursor()
    cur.execute('DROP TABLE IF EXISTS Pop_Song')
    cur.execute('''CREATE TABLE Pop_Song(ranking INTEGER, name TEXT, 
                   artist TEXT,release_date TEXT,new_release_or_not TEXT ,song_id INTEGER PRIMARY KEY)''')
    
    cur.execute('DROP TABLE IF EXISTS Lyrics')
    cur.execute('CREATE TABLE Lyrics(song_name TEXT,lyrics TEXT,song_id INTEGER PRIMARY KEY)')
    
    cur.execute('DROP TABLE IF EXISTS Collection')
    cur.execute('CREATE TABLE Collection(song_name TEXT,collection TEXT,collection_price FLOAT,track_count INTEGER,mean_price_each_song FLOAT,song_id INTEGER PRIMARY KEY)')
    conn.commit()
    conn.close()
    
    # store data into tables
    
    conn = sqlite3.connect('pop_music_remote.db')
    cur=conn.cursor()
    for s in song_list:
        # Pop_Song
        cur.execute('INSERT INTO Pop_Song (ranking,name,artist,release_date,new_release_or_not) VALUES (?,?,?,?,?)', (s['ranking'],s['name'],s['artist'],s['release_date'],s['new release or not']))
        
        #Lyrics
        # use lyrics api
        if len(s['name'].split('('))>1:
            s['track']=s['name'].split('(')[0]
        else:
            s['track']=s['name']
        lyrics_url = api_lyrics_endpt+s['artist']+'/'+s['track']
        try:    
            r_lyrics = requests.get(lyrics_url)
            json_lyrics = json.loads(r_lyrics.content)
        except:
            s['lyrics']='Not found from api'
            cur.execute('INSERT INTO Lyrics (song_name,lyrics) VALUES (?,?)', (s['name'],s['lyrics']))
            continue
        try:
            lyric_v1=''
            for l1 in json_lyrics['lyrics'].split('\n'):#handling with comma,\n and \r
                lyric_v1=lyric_v1+' '+l1
            lyric_v2=''
            for l2 in lyric_v1.split('\r'):
                lyric_v2=lyric_v2+' '+l2 
            lyric_v3=''
            for l3 in lyric_v2.split(','):
                lyric_v3=lyric_v3+l3+';'
        except:
            lyric_v3='Not found from api'
        s['lyrics']=lyric_v3
        cur.execute('INSERT INTO Lyrics (song_name,lyrics) VALUES (?,?)', (s['name'],s['lyrics']))
        
        # Collection
    for s in song_list:
        if len(s['name'].split('('))>1:
            s['track']=s['name'].split('(')[0]
        else:
            s['track']=s['name']
        itunes_url_1 = api_itunes_endpt+s['artist']+'+'+s['track']
        itunes_url_2 = api_itunes_endpt+s['artist']
        itunes_url_3 = api_itunes_endpt+s['track']#back-up searching urls 
        try:
            r_itunes = requests.get(itunes_url_1)
            json_itunes = json.loads(r_itunes.content)
        except:
            try:
                r_itunes = requests.get(itunes_url_2)
                json_itunes = json.loads(r_itunes.content)
            except:
                try:
                    r_itunes = requests.get(itunes_url_3)
                    json_itunes = json.loads(r_itunes.content)
                except:
                    s['collection']='Not found from api'
                    s['collectionPrice']=0
                    s['TrackCount']=-1
                    s['mean_price_each_song']=0
                    cur.execute('INSERT INTO Collection (song_name,collection,collection_price,track_count,mean_price_each_song) VALUES (?,?,?,?,?)', (s['name'],s['collection'],s['collectionPrice'],s['TrackCount'], s['mean_price_each_song']))
                    continue
        try:
            s['collection']=json_itunes['results'][0]['collectionName']
            s['collectionPrice']=json_itunes['results'][0]['collectionPrice']
            s['TrackCount']=json_itunes['results'][0]['trackCount']
        except:
            s['collection']='Not found from api'
            s['collectionPrice']=0
            s['TrackCount']=-1
            s['mean_price_each_song']=0
        if len(s['collection'].split(','))>1:
            s['collection']=s['collection'].split(',')[0]+' '+s['collection'].split(',')[1]
        s['mean_price_each_song']=float(s['collectionPrice'])/float(s['TrackCount'])
        cur.execute('INSERT INTO Collection (song_name,collection,collection_price,track_count,mean_price_each_song) VALUES (?,?,?,?,?)', (s['name'],s['collection'],s['collectionPrice'],s['TrackCount'], s['mean_price_each_song']))
    conn.commit()
    conn.close()
    print('Tables successfully created and written!\n')
      
