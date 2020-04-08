# MoviePopularityPrediction
Team members: Shaohua Shen, Zhou Lu, Jianing Fu, Sizhe Liu

## Motivation of Project

Throughout the past decade, video consumption has steadily shifted from traditional cable to online streaming platforms. Services like Netflix, Hulu, and HBO NOW are growing faster than anyone can expect. Even traditional tech companies like Amazon and Apple are trying to step into the tv industry by producing their own shows on their platforms like Amazon Prime Video and Apple TV+. Predictions state that the global online video streaming market size will reach USD 184.3 billion by 2027[1], and the key to success and gaining more subscriptions is to produce and stream good quality TV shows/moives. There is an increasing amount of interest in predicting a show’s quality on social media, but not a lot of research has been conducted using machine learning. Therefore, we deem it worthwhile to see how machine learning techniques, such as neural networks, can lead to better prediction for quality shows/movies.


## Dataset and Pre-Processing
Our source is from the IMDb Dataset[2] and the OMDb API[3]. We first pulled a list of every IMDb entry with their basic information including formats, title, releasing dates, length, etc. Within nearly 10 million entries, we filtered out all the entries that has less than 5000 counts of ratings since fewer number of rating might be bias so that cannot be a good measurement. We also filter out entires produced before year 2000 since the audience's taste would change with time.
Detailed information of the filtered dataset was pulled from the OMDb API, giving 10,489 entries.

### Dataset Features
There are x features in the dataset:
1. "title", 
2. "year", 
3. "rated", 
4. "released", 
5. "runtime", 
6. "genre", 
7. "director", 
8. "writer", 
9. "actors", 
10. "awards", 
11. "ratings", 
12. "metascore", 
13. "imdb_rating", 
14. "imdb_votes", 
15. "imdb_id", 
16. "type", 
17. "dvd", 
18. "box_office", 
19. "production", 
20. "website", 
21. "plot",
22. "poster",
23. "language",
24. "country"

This project is trying to predict the entry's "imdb_rating" by other given information.

### Dataset Visualization
### Data Pre-Processing
#### Irrelevent Features
"Plot", "Poster", "Language", and "Country" was deleted from the dataset since it's hard to analysis or might be discriminative.
Features that are irrelvant to the analysis were also dropped including title, imdb_id, imdb_votes, box_office, website, release date.
ratings, metascore, and awards were dropped since the movies/shows that we are trying to predict would not have these information before they were aired.

#### Feature Quantization 
We quatized features including "rated", "actors", "director", "writer" by calculating the mean imdb_rating of each category/person's work and normalized from 0 to 10.0.

#### Feature Analysis
After quantize the features, we plot the following correlation matrix and covariance matrix to show their relationships:

## Methods
### Neural Network

## Conclusion

## Reference

[1]“Video Streaming Market Worth $184.3 Billion By 2027: CAGR: 20.4%.” Market Research Reports & Consulting, www.grandviewresearch.com/press-release/global-video-streaming-market.

[2] https://www.imdb.com/interfaces/  https://datasets.imdbws.com/

[3] http://www.omdbapi.com/
