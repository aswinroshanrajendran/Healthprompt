# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Dict

# router = APIRouter()

# class NERRequest(BaseModel):
#     text: str

# @router.post("/ner/")
# async def run_ner(request: NERRequest) -> Dict[str, str]:
#     # For now, just return a simple response confirming the received text
#     received_text = request.text
#     return {"message": "Text received for NER", "received_text": received_text}

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Union
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

router = APIRouter()

class NERRequest(BaseModel):
    text: str

class NERResponse(BaseModel):
    tokens: List[str]
    labels: List[str]

# Load the model and tokenizer
model_path = r"D:\LEGION\Documents\Master - EPITA\S3\Action Learning\clinicalbert_finetunned\clinicalbert_finetunned\checkpoint-624"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

def predict_ner(text: str) -> NERResponse:
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt")

    # Get model predictions
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)

    # Decode the predictions
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze().tolist())
    labels = [model.config.id2label[pred.item()] for pred in predictions.squeeze()]

    return NERResponse(tokens=tokens, labels=labels)

@router.post("/ner/", response_model=NERResponse)
async def run_ner(request: NERRequest) -> NERResponse:
    # Predict NER labels for the input text
    ner_result = predict_ner(request.text)
    return ner_result
