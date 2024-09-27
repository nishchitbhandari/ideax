from pydantic import BaseModel
from typing import List, Dict

# Define the request body model using Pydantic
class UserHistoryRequest(BaseModel):
    user_history: List[str]  # A dictionary where keys are video_ids and values are watch counts
    n_recommendations: int = 10   # Default to 10 recommendations

# Define the response model for recommendations
class RecommendationResponse(BaseModel):
    recommendations: List[str]  # A list of recommended video IDs

