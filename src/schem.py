from pydantic import BaseModel
from typing import List, Literal

class CreateWorkItemRequest(BaseModel):
    title: str
    description: str
    acceptanceCriteria: List[str]
    workItemType: Literal["PBI", "Bug", "Task"] = "PBI"

class CreateWorkItemResponse(BaseModel):
    id: int
    url: str
    title: str
