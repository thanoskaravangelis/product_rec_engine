from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json

# Connect to Redis
cache = redis.Redis(host='localhost', port=6379, db=0)

class RecommendationRequest(BaseModel):
    user_id: int
    n_recommendations: int = 5

class BatchRecommendationRequest(BaseModel):
    user_ids: list[int]
    n_recommendations: int = 5

app = FastAPI()

@app.post("/recommendations/")
def get_recommendations(request: RecommendationRequest):
    user_id = request.user_id
    n_recommendations = request.n_recommendations

    # Check if results are cached
    cache_key = f"recommendations:{user_id}:{n_recommendations}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    raise HTTPException(status_code=404, detail=f"Recommendations for user {user_id} not found.")

@app.post("/batch_recommendations/")
def batch_recommendations(request: BatchRecommendationRequest):
    user_ids = request.user_ids
    n_recommendations = request.n_recommendations

    results = []
    for user_id in user_ids:
        cache_key = f"recommendations:{user_id}:{n_recommendations}"
        cached_result = cache.get(cache_key)
        if cached_result:
            results.append(json.loads(cached_result))
        else:
            results.append({"user_id": user_id, "recommended_items": []})

    return {"recommendations": results}
