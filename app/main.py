from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from app.pipeline import PreProcessingPipeline

app = FastAPI()
pipeline = PreProcessingPipeline("config/pipeline_config.json")

class LLMRequest(BaseModel):
    query: str

@app.post("/process")
async def process_request(request: LLMRequest) -> Dict[str, Any]:
    try:
        processed_context = pipeline.execute(request.dict())
        return {"processed_data": processed_context}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))