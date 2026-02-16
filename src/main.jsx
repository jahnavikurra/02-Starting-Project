from fastapi import FastAPI, HTTPException
from src.models.schemas import CreateWorkItemRequest, CreateWorkItemResponse
from src.services.ado import create_work_item

app = FastAPI()

@app.post("/api/workitems/create", response_model=CreateWorkItemResponse)
def create(req: CreateWorkItemRequest):
    try:
        result = create_work_item(
            title=req.title,
            description_md=req.description,
            acceptance_criteria=req.acceptanceCriteria,
            work_item_type=req.workItemType,
        )
        return CreateWorkItemResponse(
            id=int(result["id"]),
            url=result["_links"]["html"]["href"],
            title=result["fields"]["System.Title"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
