# api.py
from fastapi import FastAPI, HTTPException
from main import get_weighted_recommendations
from schema import *
from fastapi.middleware.cors import CORSMiddleware

# FastAPI app instance
app = FastAPI()

# Create a POST endpoint to accept user history and return recommendations
@app.post("/recommendations", response_model=RecommendationResponse)
def get_recommendations(request: UserHistoryRequest):
    print("Reached here")
    try:
        # Call the recommendation function from main.py
        recommendations = get_weighted_recommendations(
            user_history=request.user_history,
            n_recommendations=request.n_recommendations
        )
        return RecommendationResponse(recommendations=recommendations)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
