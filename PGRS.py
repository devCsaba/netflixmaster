from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

from collections import defaultdict
from scipy.spatial.distance import cosine
from sklearn.metrics import silhouette_score
import math
import json


class PGRS:
    def __init__(self):
        self.processed_data = pd.read_csv("processed_dataset.csv")
        self.movies_data = pd.read_csv("movies2.csv")
        self.clustered_data = pd.read_csv("clustered_data_v2.csv")

        self.processed_data = self.processed_data.set_index('id', drop=True).drop('title', axis=1)
        self.processed_data = self.processed_data.drop(["vote_average", "vote_count", "release_date", "revenue", "runtime", "budget", "popularity"], axis=1)

        ids = self.movies_data["id"]
        titles = self.movies_data["title"]
        self.movie_title_dict = dict(zip(ids, titles))

    def recommend_on_watch_history(self, watch_history, k=4):
        
        if all(isinstance(item, int) for item in watch_history):
            pass
        elif all(isinstance(item, str) for item in watch_history):
            watch_history = [self.get_movie_id(movie_title) for movie_title in watch_history]
        else:
            raise Exception("input only movie ids or movie titles")
        
        #movie_embeds = [processed_data.loc[movie_id] for movie_id in watch_history]
        movie_embeds = self.processed_data.loc[watch_history]
        
        silhouette_scores = []
        max_k = min(15, len(watch_history))
        trying_ks = [k for k in range(2, max_k)]
        for k in trying_ks:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(movie_embeds)
            score = silhouette_score(movie_embeds, kmeans.labels_)
            silhouette_scores.append(score)
        
        best_k = 0
        if len(silhouette_scores) > 0:
            best_k = 2 + np.array(silhouette_scores).argmax()
        
        recommendations_by_label = {}

        already_recommended = []
        already_recommended.extend(watch_history)

        if best_k != 0 and len(watch_history) > best_k:
        
            kmeans = KMeans(n_clusters=best_k, random_state=42)
            kmeans.fit(movie_embeds)

            labels = kmeans.labels_

            grouped_movies = defaultdict(list)
            for movie_id, label in zip(watch_history, labels):
                grouped_movies[label].append(movie_id)

            #print(grouped_movies)

            for label, movie_ids in grouped_movies.items():
                _ , recomended_ids = self.recommend_movie(movie_ids, k)

                # this one checks if movie_ids was not already recommended in other genre cluster
                recommendations_by_label[label] = []
                for recomended_id in recomended_ids:
                    if recomended_id not in already_recommended:
                        recommendations_by_label[label].append(recomended_id)
                        already_recommended.append(recomended_ids)
        
        else:
            _ , recomended_ids = self.recommend_movie(watch_history, k)
            recommendations_by_label[0] = recomended_ids
        
        # if recomendation should be empty, take more movies (k)
        is_empty = all(len(lst) == 0 for lst in recommendations_by_label.values())
        if is_empty:
            print("prazdne")
            _ , recomended_ids = self.recommend_movie(watch_history, k + 5)
            recommendations_by_label[0] = recomended_ids

        return recommendations_by_label
    

    def recommend_movie(self, inputs, k=10):
    
        if all(isinstance(item, int) for item in inputs):
            pass
        elif all(isinstance(item, str) for item in inputs):
            inputs = [self.get_movie_id(movie_title) for movie_title in inputs]
        else:
            raise Exception("input only movie ids or movie titles")
        
        df = self.processed_data.copy()
        
        cols = list(self.processed_data.columns)
        
        movie_embeds = [df.loc[movie_id] for movie_id in inputs]
        centroid = np.mean(movie_embeds, axis=0)
        
        centroid_weights = self.weights_for_centroid(movie_embeds)
        
        weighted_centorid = self.get_weighted_centorid(centroid, centroid_weights)
    
        df['distance'] = np.sqrt(((df[cols] - weighted_centorid) ** 2).sum(axis=1))
        #df['distance'] = df[cols].apply(lambda row: cosine(row.values, weighted_centorid), axis=1)

        top_k = df.nsmallest(k, 'distance')
        top_ids = list(top_k.index)
        top_ids = [item for item in top_ids if item not in inputs]
        movie_titles = [self.get_movie_title(movie_id) for movie_id in top_ids]
        return movie_titles, top_ids
    
    def weights_for_centroid(self, movie_embedds):
    
        NUMBER_OF_EMBEDDINGS = 50
        
        keyword_embedd_weights = [1] * NUMBER_OF_EMBEDDINGS
        genre_counts = []
        
        for col in range(19):
            column_values = [vector[col] for vector in movie_embedds]
            count = 1 + math.log10(1 + sum(column_values))
            genre_counts.append(count)
        return genre_counts + keyword_embedd_weights
    

    def get_weighted_centorid(self, centorid, centroid_weights):
        
        if not isinstance(centorid, np.ndarray):
            centorid = np.array(centorid)
        
        if not isinstance(centroid_weights, np.ndarray):
            centroid_weights = np.array(centroid_weights)

        weighted_centorid = centroid_weights * centorid
        
        return weighted_centorid


    def get_movie_title(self, key):
        if key in self.movie_title_dict:
            return self.movie_title_dict[key]
        else:
            return None

    def get_movie_id(self, value):
        for key, val in self.movie_title_dict.items():
            if val == value:
                return key
        return None

    def get_movies_by_partial_value(self, value):
        matching_keys = []
        for key, val in self.movie_title_dict.items():
            if value.lower() in str(val).lower():
                matching_keys.append(key)
        
        movies = [self.get_movie_title(matching_key) for matching_key in matching_keys]
        return movies
        
        