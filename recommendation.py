import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.neighbors import NearestNeighbors

class Recommender:
    def __init__(self, events_df):
        self.events = events_df
        self.user_encoder = {user: idx for idx, user in enumerate(self.events['visitorid'].unique())}
        self.item_encoder = {item: idx for idx, item in enumerate(self.events['itemid'].unique())}

        self.events['user_idx'] = self.events['visitorid'].apply(lambda x: self.user_encoder[x])
        self.events['item_idx'] = self.events['itemid'].apply(lambda x: self.item_encoder[x])

        # sparse user-item interaction matrix
        user_item_sparse = coo_matrix(
            (self.events['rating'], (self.events['user_idx'], self.events['item_idx'])),
            shape=(len(self.user_encoder), len(self.item_encoder))
        )

        # Convert to CSR 
        self.user_item_csr = user_item_sparse.tocsr()

        self.knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
        self.knn.fit(self.user_item_csr)

    def get_user_recommendations(self, user_id, n_recommendations=5):
        if user_id not in self.user_encoder:
            raise ValueError(f"User ID {user_id} not found in data.")

        user_idx = self.user_encoder[user_id]
        user_vector = self.user_item_csr[user_idx]

        distances, neighbors = self.knn.kneighbors(user_vector, n_neighbors=10)
        neighbors = neighbors.flatten()

        similar_users_ratings = self.user_item_csr[neighbors].toarray()
        user_similarities = 1 - distances

        user_similarities = user_similarities.reshape(-1, 1)

        weighted_ratings = (similar_users_ratings.T @ user_similarities).flatten()

        sum_similarities = user_similarities.sum()
        weighted_ratings /= sum_similarities + 1e-9  # Add small epsilon to prevent division by zero

        user_rated_items = self.user_item_csr[user_idx].toarray().flatten()
        weighted_ratings[user_rated_items > 0] = 0

        top_indices = weighted_ratings.argsort()[::-1][:n_recommendations]
        recommendations = [list(self.item_encoder.keys())[idx] for idx in top_indices]

        return recommendations