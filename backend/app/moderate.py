from fastapi import APIRouter, UploadFile, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db import get_db
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

load_dotenv()

router = APIRouter()

CONTENT_SAFETY_ENDPOINT = os.getenv("CONTENT_SAFETY_ENDPOINT")
CONTENT_SAFETY_KEY = os.getenv("CONTENT_SAFETY_KEY")

async def verify_token(
    authorization: str = Header(...),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    token_doc = await db.tokens.find_one({"token": token})
    
    if not token_doc:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token

def severity_to_percentage(severity: int) -> float:
    return round(severity / 7.0, 2)

async def analyze_image_content(image_data: bytes) -> dict:
    if not CONTENT_SAFETY_ENDPOINT or not CONTENT_SAFETY_KEY:
        raise HTTPException(status_code=500, detail="Azure Content Safety not configured")
    
    try:
        # Create Content Safety Client
        client = ContentSafetyClient(
            CONTENT_SAFETY_ENDPOINT, 
            AzureKeyCredential(CONTENT_SAFETY_KEY)
        )

        request = AnalyzeImageOptions(image=ImageData(content=image_data))
        response = client.analyze_image(request)
        
        result = {
            "hate": severity_to_percentage(
                next((item.severity for item in response.categories_analysis 
                     if item.category == "Hate"), 0)
            ),
            "self_harm": severity_to_percentage(
                next((item.severity for item in response.categories_analysis 
                     if item.category == "SelfHarm"), 0)
            ),
            "sexual": severity_to_percentage(
                next((item.severity for item in response.categories_analysis 
                     if item.category == "Sexual"), 0)
            ),
            "violence": severity_to_percentage(
                next((item.severity for item in response.categories_analysis 
                     if item.category == "Violence"), 0)
            )
        }
        return result
        
    except HttpResponseError as e:
        error_detail = f"{e.error.code}: {e.error.message}" if e.error else str(e)
        raise HTTPException(status_code=400, detail=f"Azure Content Safety error: {error_detail}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing image: {str(e)}")

@router.post("/moderate")
async def moderate_image(
    file: UploadFile,
    token: str = Depends(verify_token)):
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_data = await file.read()
        
        
        analysis_result = await analyze_image_content(image_data)
        
        return JSONResponse(content={
            "result": analysis_result, 
        })
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")