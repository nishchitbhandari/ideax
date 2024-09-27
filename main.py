from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from query import get_all_users

def get_weighted_recommendations(user_history, n_recommendations=10):
    # Load the dataset (replace with your actual data loading logic)
    dataset = get_all_users()

    # Ensure the dataset has 'Id' and 'Subject speciality' columns
    if 'Id' not in dataset.columns or 'Subject speciality' not in dataset.columns:
        raise KeyError("Dataset must contain 'Id' and 'Subject speciality' columns.")
    
    # Convert user_history (list of string 'Id's) to actual IDs in the dataset
    user_history_ids = user_history  # Already in string format

    # Convert the user_history to a counter (to account for watch counts if needed)
    user_history = dict(Counter(user_history_ids))

    # Prepare the TF-IDF vectorizer for the 'Subject speciality' column
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(dataset['Subject speciality'])

    # Calculate the cosine similarity between each individual's subject speciality
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Initialize a dictionary to hold weighted similarity scores
    weighted_scores = {}

    # Count the total number of videos watched by the user in each subject category
    category_count = {}
    total_views = sum(user_history.values())

    # Build category count based on the user's viewing history
    for video_id, count in user_history.items():
        video_idx = dataset.index[dataset['Id'] == video_id][0]  # Find index of the video
        subject_category = dataset['Subject speciality'].iloc[video_idx]
        if subject_category in category_count:
            category_count[subject_category] += count
        else:
            category_count[subject_category] = count

    # Calculate the percentage of views per category
    category_percentages = {cat: count / total_views for cat, count in category_count.items()}

    # Initialize a dictionary to store the number of recommendations per category
    category_recommendation_count = {cat: round(percentage * n_recommendations) for cat, percentage in category_percentages.items()}

    # Ensure that the total recommendations match `n_recommendations`
    total_recommendations = sum(category_recommendation_count.values())
    if total_recommendations < n_recommendations:
        # Distribute remaining recommendations evenly to the largest categories
        for _ in range(n_recommendations - total_recommendations):
            max_category = max(category_recommendation_count, key=category_recommendation_count.get)
            category_recommendation_count[max_category] += 1

    # Dictionary to store recommendations for each category
    recommendations = []

    # Iterate through the user's history to calculate similarity scores and aggregate recommendations
    for video_id, weight in user_history.items():
        video_idx = dataset.index[dataset['Id'] == video_id][0]  # Find index of the video
        sim_scores = cosine_sim[video_idx]
        
        for i, score in enumerate(sim_scores):
            # Only add the similarity score if it's a different video and the user hasn't already watched it
            if dataset['Id'].iloc[i] not in user_history and score > 0:
                subject_category = dataset['Subject speciality'].iloc[i]
                if subject_category not in weighted_scores:
                    weighted_scores[subject_category] = []
                weighted_scores[subject_category].append((dataset['Id'].iloc[i], score))  # Store string ID and similarity score

    # For each category, sort the recommendations by similarity score and select the top N recommendations
    for category, count in category_recommendation_count.items():
        if category in weighted_scores:
            # Sort by similarity score (descending) and take the top 'count' recommendations
            sorted_videos = sorted(weighted_scores[category], key=lambda x: x[1], reverse=True)
            recommendations.extend([video[0] for video in sorted_videos[:count]])

    # Return final recommendations as string 'Id's
    return recommendations[:n_recommendations]
