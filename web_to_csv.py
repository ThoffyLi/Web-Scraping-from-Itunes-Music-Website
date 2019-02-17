# This function is for scraping the information of pop songs, get data from api and finally store these information into separate csv files.
# The input is web url, endpoint of lyrics and itunes api(remote); the output are three csv files(local).

import requests
from bs4 import BeautifulSoup as BS
import bs4
import json

 
def web_to_csv(web_url,api_lyrics_endpt,api_itunes_endpt):
    def getr(u):
        try:
            r = requests.get(u,timeout=30)
            r.raise_for_status()
        except:
            print("error")
        return r
    
    # 1. scrape web data
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
            song['new_release_or_not']='New'
        else:
            song['release_date']=s.findAll('li')[1].text.split(':')[1].split(',')[0]+s.findAll('li')[1].text.split(':')[1].split(',')[1]
            song['new_release_or_not']='Not New'        
        song_list.append(song)
        ranking=ranking+1   
        
        
    # write scraped data to csv
    pop_song_file = open('pop_song.csv','w',encoding='utf-8')
    new_header_str = ''
    fields = list(song_list[0].keys())#headers
    for f in fields:
        new_header_str = new_header_str+f+','
    new_header_str =  new_header_str[:-1]
    new_header_str =  new_header_str + '\n'
    pop_song_file.write(new_header_str)
    
    new_rest_str = ''#rest data
    for s in song_list:
        new_rest_str = new_rest_str + str(s['ranking']) +','+s['name']+','+s['artist']+','+s['release_date']+','+s['new_release_or_not']+'\n'
    pop_song_file.write(new_rest_str)
    print("scraped data writing successfully to csv! Please waiting for the remaining two files......")
    pop_song_file.close()
    
    
    # 2. write lyrics data extracted from lyrics api to a csv
    lyrics_file = open('lyrics.csv','w',encoding='utf-8-sig') 
    lyrics_header_str='song_name,lyrics,song_id\n'
    lyrics_file.write(lyrics_header_str)
    lyrics_rest_str=''
    for s in song_list:
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
            lyrics_rest_str=lyrics_rest_str + s['name']+','+s['lyrics']+','+str(s['ranking'])+'\n'
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
        lyrics_rest_str=lyrics_rest_str + s['name']+','+s['lyrics']+','+str(s['ranking'])+'\n'
    lyrics_file.write(lyrics_rest_str)
    print('Lyrics api data writing successfully to csv!Please waiting for the last file......')
    lyrics_file.close()

 # 3. write collection data extracted from itunes api to a csv
    itunes_file = open('itunes.csv','w',encoding='utf-8-sig')
    itunes_header_str = 'song_name,collection,collection_price,track_count,mean_price_each_song,song_id\n'
    itunes_file.write(itunes_header_str)
    itunes_rest_str=''
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
                    s['TrackCount']=-2
                    s['mean_price_each_song']=0
                    itunes_rest_str=itunes_rest_str+s['name']+','+s['collection']+','+str(s['collectionPrice'])+','+str(s['TrackCount'])+','+str(s['mean_price_each_song'])+','+str(s['ranking'])+'\n'
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
        itunes_rest_str=itunes_rest_str+s['name']+','+s['collection']+','+str(s['collectionPrice'])+','+str(s['TrackCount'])+','+str(s['mean_price_each_song'])+','+str(s['ranking'])+'\n'
    itunes_file.write(itunes_rest_str)
    print('Itunes api data writing successfully to csv! All done!\n')
    itunes_file.close()
   

 