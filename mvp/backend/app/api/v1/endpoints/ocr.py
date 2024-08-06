from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict, List
import requests
from  . import API_KEY_OCR
router = APIRouter()

@router.post("/ocr/")
async def perform_ocr(file: UploadFile = File(...)) -> Dict[str, str]:

    ocr_api_url = "https://api.api-ninjas.com/v1/imagetotext"
    headers = {"X-Api-Key": API_KEY_OCR}  

    # Read the file content
    image_data = await file.read()

    # Log file content type and size
    mime_type = file.content_type or "image/jpeg"  # Default to image/jpeg if None
    print(f"File content type: {mime_type}")
    print(f"File size: {len(image_data)} bytes")

    # Send the file to the OCR API
    response = requests.post(
        ocr_api_url,
        headers=headers,
        files={"image": (file.filename, image_data, mime_type)}
    )

    print(f"Request sent to {ocr_api_url} with headers {headers}")

    # Check if the request was successful
    if response.status_code != 200:
        print(f"OCR API response status code: {response.status_code}")
        print(f"OCR API response text: {response.text}")
        raise HTTPException(status_code=response.status_code, detail=f"OCR API request failed with status code {response.status_code}")

    # Log the response text for debugging
    print(response.text)

    # Process the response as a list of dictionaries
    result = response.json()
    texts = [item['text'] for item in result] if isinstance(result, list) else ["No text found"]
    print(f"OCR API response JSON: {texts}")

    return {"text": " ".join(texts)}  # Join all text fragments into a single string


