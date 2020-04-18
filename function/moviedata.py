import csv
import omdb
import json

"""
https://datasets.imdbws.com/
http://www.omdbapi.com/?apikey=86208057&
http://www.omdbapi.com/?apikey=86208057&i=tt2008120&r=xml
example: https://github.gatech.edu/pages/avitankar3/music-popularity.github.io/
"""

omdb.set_default('apikey', 'f9001726')
d = {}

with open("title.ratings.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    next(tsvreader)
    count = 0
    for line in tsvreader:
      if int(line[2]) > 5000:
        data = omdb.imdbid(line[0])
        if int(data['year'][:4]) > 2000 and data['imdb_raing'] != "N/A":
          d[line[0]] = data
          count += 1
print(count)
file = open("moviedata.txt", "w")
for key in d.keys():
    file.writelines(json.dumps(d[key]) + "\n")
file.close()