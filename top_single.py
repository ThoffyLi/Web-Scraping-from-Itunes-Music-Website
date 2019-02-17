import sqlite3

def top_single(db_name):
    conn= sqlite3.connect(db_name)
    cur=conn.cursor()
    cur.execute('''SELECT c.collection,p.artist,p.release_date,l.lyrics FROM Pop_Song p INNER JOIN Collection c INNER JOIN Lyrics l ON (p.ranking=c.song_id AND c.song_id=l.song_id)
               WHERE c.track_count=? ORDER BY p.ranking''',(1,))
    top_single = cur.fetchall()[0]
    print("The best single:\n")
    print('name:'+' '+top_single[0]+'\n')
    print('artist:'+' '+top_single[1]+'\n')
    print('release date:'+' '+top_single[2]+'\n')
    print('lyrics:'+' '+top_single[3]+'\n')
    conn.commit()
    conn.close()
 
 
 

