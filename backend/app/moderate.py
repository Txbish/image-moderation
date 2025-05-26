from fastapi import APIRouter, UploadFile, File
import random

router = APIRouter()

@router.post("/moderate")
async def moderate_image(file: UploadFile = File(...)):
    # Fake moderation scores
    scores = {
        "nudity": round(random.uniform(0, 1), 2),
        "violence": round(random.uniform(0, 1), 2),
        "self_harm": round(random.uniform(0, 1), 2)
    }
    return {"result": scores}
