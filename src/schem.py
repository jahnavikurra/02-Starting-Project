from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# ---------- Validate ----------
class ValidateRequest(BaseModel):
    notesText: str = Field(..., min_length=1)

class ValidateResponse(BaseModel):
    valid: bool
    reason: str
    requiredQuestions: List[str] = []
    confidence: Optional[float] = None


# ---------- Generate ----------
class GenerateRequest(BaseModel):
    notesText: str = Field(..., min_length=1)
    workItemType: Literal["PBI", "Bug", "Task"] = "PBI"
    process: Literal["Scrum", "Agile"] = "Scrum"

class WorkItemDraft(BaseModel):
    title: str
    description: str
    acceptanceCriteria: List[str] = []
    tasks: List[str] = []
    assumptions: List[str] = []
    confidence: Optional[float] = None


# ---------- Create Work Item (optional) ----------
class CreateWorkItemRequest(BaseModel):
    title: str
    description: str
    acceptanceCriteria: List[str] = []
    workItemType: Literal["PBI", "Bug", "Task"] = "PBI"

class CreateWorkItemResponse(BaseModel):
    id: int
    url: str
    title: str
