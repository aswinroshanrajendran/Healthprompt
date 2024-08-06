from fastapi import APIRouter, HTTPException, Body
from typing import Dict
import http.client
from . import API_KEY_TRANSLATE
import json


router = APIRouter()

@router.post("/translate/")
async def translate_text(
    text: str = Body(...),
    target_language: str = Body(...),
    source_language: str = Body('en')  # Default source language is English
) -> Dict[str, str]:
    conn = http.client.HTTPSConnection("text-translator2.p.rapidapi.com")

    payload = (
        "-----011000010111000001101001\r\n"
        f"Content-Disposition: form-data; name=\"source_language\"\r\n\r\n{source_language}\r\n"
        "-----011000010111000001101001\r\n"
        f"Content-Disposition: form-data; name=\"target_language\"\r\n\r\n{target_language}\r\n"
        "-----011000010111000001101001\r\n"
        f"Content-Disposition: form-data; name=\"text\"\r\n\r\n{text}\r\n"
        "-----011000010111000001101001--\r\n\r\n"
    )

    headers = {
        'x-rapidapi-key': API_KEY_TRANSLATE,  # Replace with your actual RapidAPI key
        'x-rapidapi-host': "text-translator2.p.rapidapi.com",
        'Content-Type': "multipart/form-data; boundary=---011000010111000001101001"
    }

    try:
        conn.request("POST", "/translate", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        result = json.loads(data)

        if result.get("status") == "success":
            translated_text = result["data"]["translatedText"]
            return {"translated_text": translated_text}
        else:
            raise HTTPException(status_code=500, detail="Translation failed")
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
