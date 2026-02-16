from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# ==============================
# Request: Generate AI Work Item
# ==============================
class GenerateRequest(BaseModel):
    notesText: str = Field(..., min_length=5)
    workItemType: Literal["PBI", "Bug", "Task"] = "PBI"
    process: Literal["Scrum", "Agile"] = "Scrum"


# ==============================
# Response: AI Generated Draft
# ==============================
class WorkItemDraft(BaseModel):
    title: str
    description: str
    acceptanceCriteria: List[str] = []
    tasks: List[str] = []
    assumptions: List[str] = []
    confidence: Optional[float] = None


# ==============================
# Request: Create Work Item in ADO
# ==============================
class CreateWorkItemRequest(BaseModel):
    title: str
    description: str
    acceptanceCriteria: List[str]
    workItemType: Literal["PBI", "Bug", "Task"]


# ==============================
# Response: Created Work Item
# ==============================
class CreateWorkItemResponse(BaseModel):
    id: int
    url: str
    title: str


# ==============================
# Error
# ==============================
class ErrorResponse(BaseModel):
    detail: str
