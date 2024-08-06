from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict
import requests
from . import API_KEY_OCR
router = APIRouter()

@router.get("/test/")
def test_endpoint():
    return {"message": "Test successful"}
