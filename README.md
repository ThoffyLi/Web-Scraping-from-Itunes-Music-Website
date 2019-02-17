1. How to run your code (what command-line switches they are, what happens when you
invoke the code, etc.)

The main file of my program is 'LI_YUAN_hw6.py'. To run the program, just run this file directly, 
and there will be a sequence of choices to make, here I am going to explain each one in detail:

1) Do you want to acquire csv files from web first?
Input 'Y' or 'N'(any other input will be warned as invalid and requested to reinput)
When first get this program, we don't have any data. Then there are two ways to build the 
data model: remote and local. For local method, we should choose 'Y' to get data from the 
web and apis and store them locally as csv files(as intermediate data).
If we prefer remote method, here 'N' should be the right choice since no local files are needed. 

PS:The running of this step might take a while.

2) Please choose how to build data model! input "remote" or "local":
Input 'remote' or 'local'(any other input will be warned as invalid and requested to reinput)
This is for choosing the model-building method, as metioned before. If in the previous question, we
select 'N' which means there are no local files for modeling, here choosing 'remote' is able to
build the data model directly from web and apis. If local files exist in the working directory(achieved
from the previous step), here 'local' is a more efficient choice(remote also works here, but slower). 
Another situation is that if we chose 'N' previously and have no local files, then we still choose 'local'
here, the program will identify this contradiction and automatically select 'remote'. 
The output for either input is the same db file with three tables(Pop_Song,Lyrics,Collection).

3) Show the information and lyrics of the best single song?
From here, we start conclusion part. This is not the final conclusion, but just a simple manipulation of
the data model from HW5. Choose 'Y' to show the result, or 'N' to skip it.

4)Show the final conclusions?
Input'Y' to see the final conclusions, which are made up of some statistical computing and visualizations.
There will be three graphs shown one by one(the next shows right after you close the current one).

   


2. Any major ¡°gotchas¡± to the code (i.e. things that don¡¯t work, go slowly, could be
improved, etc.)

1) I chose a web of pop song ranking that changes every day with new songs superceding old ones.
Then there's a problem, the two apis might find it hard to provide information for some latest pop
songs, since they are brand new! But so far in my testing cases, this is not a big problem and doesn't 
affect the final result too much.
  
2) I have to admit that when I worked on homework5, I didn't genuinely feel the tardiness and inflexibility
of dict-csv based storing as an intermediate data. Then in the process of manipulating data and concluding,
I found this problem and changed the later part to use pandas data frame, it was much more convenient and taught me a lesson.
 



3. Anything else you feel is relevant to the grading of your project.

Since the most important thing of grading this project is that code works, I've tested many times on both windows 
and ios and this code works well. So if there is  confusion about running the code or occasional malfunction 
of the itunes api(very rare, but it might happen;run it again would work), please contact me yli456@usc.edu.
 



4. What did you set out to study? (i.e. what was the point of your project? This should be
close to your HW3 assignment, but if you switched gears or changed things, note it
here.)

I'm a crazy fan of pop music, so I've alway been curious about those top collections on itunes ranking. This project analyzes
2018 top 100 pop music, and enrich it with two apis(itunes information and lyrics). 

When there is just one track in a collection, the song's a single. There are singles and non-singles in the 
ranking list. Often, when a singer release a new song as a single, we may think of it as an emphasis which means 
this song has higher quality and fans shouldn't miss it! Is this really the case? This question has realistic significance 
especially for the pop music fans, because based on the conclusion,they can make the better decision on which collections 
their money should go to, single or collections with many tracks. 

To answer the question, this project is interested in exploring the difference of quality and price bewtween singles and non-single songs.
To quantify, the solution will try to break through on their difference in terms of price_per_song and rankings.

The results will be presented in the form of statistical computing and visualization.




5. What did you Discover/what were your conclusions (i.e. what were your findings? Were
your original assumptions confirmed, etc.?)

The result of the project leads to two conclusions:
1) from the line graph, we can see that single songs have very uniform each_song_mean_price of $1.29 while non-singles songs are obviously cheaper 
and variant(although some outliers). This means pop music industry is very likely to have a standard price for single songs which is higher than non-single songs.

2)Then from bar plots of price and ranking difference between single and non-single songs, our assumption is confirmed£ºthe mean price of single songs
is approximately 1.25, higher than non-single ones with the price of only 0.76 each song(here the number may not be fixed, because the rankings are
changing every day, so when you run the code, all the data are real-time, and the conclusion may even change slightly). Also, the average ranking of single songs and non-singles
are approximately the same. 

All in all, the conclusion based on the study is that single songs are of higher quality and price than non-single ones. When a collection is released with
just one song in it, the singer may be sending the signal: I worked very hard on this song, it's a upmarket, buy it!
 


6. What would you do ¡°next¡± to expand or augment the project?

1) Enrich the conclusion with the data of release to show the comparison of ranking between old and new songs. 
2) Design user interface for this program.