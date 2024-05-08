import pandas as pd
from sklearn.model_selection import train_test_split
from recommendation import Recommender
import csv
import redis

# Load RetailRocket events data
events = pd.read_csv('data/events.csv')

# Filter for 'view' and 'transaction' events
interaction_types = ['view', 'transaction']
filtered_events = events[events['event'].isin(interaction_types)]
filtered_events['rating'] = filtered_events['event'].apply(lambda x: 1 if x == 'view' else 5)

train_events, test_events = train_test_split(filtered_events, test_size=0.2, random_state=42)

# Train
recommender = Recommender(train_events)

# Generate recommendations for training users
test_users = test_events['visitorid'].unique()
recommendations = []

for user_id in test_users:
    try:
        recommended_items = recommender.get_user_recommendations(user_id, n_recommendations=5)
        recommendations.append({'user_id': user_id, 'recommended_items': recommended_items})
    except ValueError:
        continue

# Save recommendations to CSV
with open('recommendations.csv', 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'recommended_items']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for rec in recommendations:
        writer.writerow({'user_id': rec['user_id'], 'recommended_items': ','.join(map(str, rec['recommended_items']))})

# Load recommendations into Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

with open('recommendations.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        user_id = row['user_id']
        recommended_items = row['recommended_items']
        cache_key = f"recommendations:{user_id}:5"
        cache.set(cache_key, f'{{"user_id": {user_id}, "recommended_items": [{recommended_items}]}}', ex=3600)
