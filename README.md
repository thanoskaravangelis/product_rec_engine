# RetailRocket Recommendation Engine

This project implements a recommendation engine for an e-commerce platform using the RetailRocket dataset. The engine is designed to provide personalized product recommendations to users based on their browsing and purchase history.

## Features
- **Collaborative Filtering Model**: Nearest neighbors-based collaborative filtering.
- **FastAPI RESTful API**: Easily integrate recommendations via API.
- **Scalability & Performance**: Results are cached using Redis.

## Requirements
- Python 3.8+
- Docker (for Redis installation via Docker)
- RetailRocket Dataset (Download from [Kaggle](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset))

## Setup and Installation

1. **Clone the Repository**:

```bash
git clone <repository_url>
cd retailrocket-recommendation-engine
```

2.  **Install dependencies**
pip3 install -r requirements.txt

3. **Install Redis**:
Docker:
```bash
docker run -d -p 6379:6379 redis
```

4. **Train model**
```bash
python3 main.py
```

## Usage
Start the FastAPI Server
Run the FastAPI server:
```bash
uvicorn api:app --reload
```
The API will be available at http://127.0.0.1:8000.

### API Endpoints
1. **/recommendations/ [POST]**

Description: Returns product recommendations for a given user.

Request Body:

```json
{
    "user_id": 12345,
    "n_recommendations": 5
}
```

Response:

```json
{
    "user_id": 12345,
    "recommended_items": [67890, 54321, 12345, 98765, 23456]
}
```

2. **/batch_recommendations/ [POST]**

Description: Returns batch recommendations for a list of user IDs.

Request Body:

```json
{
    "user_ids": [12345, 67890],
    "n_recommendations": 5
}```
Response:

```json

{
    "recommendations": [
        {"user_id": 12345, "recommended_items": [67890, 54321, 12345, 98765, 23456]},
        {"user_id": 67890, "recommended_items": [54321, 67890, 23456, 98765, 12345]}
    ]
}```