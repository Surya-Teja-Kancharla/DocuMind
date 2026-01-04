from pydantic import BaseModel
from typing import Dict

class IngestedDocument(BaseModel):
    document_id: str
    filename: str
    content: str
    metadata: Dict
