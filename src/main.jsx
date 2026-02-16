from fastapi import FastAPI, HTTPException

from src.models.schemas import (
    ValidateRequest, ValidateResponse,
    GenerateRequest, WorkItemDraft,
    CreateWorkItemRequest, CreateWorkItemResponse,
)
from src.utils.validator import validate_notes_text
from src.services.llm_gate import gate_validate_notes
from src.services.llm import generate_work_item_draft
from src.services.ado import create_work_item

app = FastAPI(
    swagger_js_url="/static/swagger-ui-bundle.js",
    swagger_css_url="/static/swagger-ui.css",
    title="AI WorkItems Backend")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/validate", response_model=ValidateResponse)
def validate(req: ValidateRequest):
    ok, msg = validate_notes_text(req.notesText)
    if not ok:
        return ValidateResponse(
            valid=False,
            reason=msg,
            requiredQuestions=[
                "What is the goal/problem?",
                "What should happen (expected behavior)?",
                "Who is the user/persona?",
                "Any constraints/scope?",
            ],
            confidence=0.0,
        )

    gate = gate_validate_notes(req.notesText)
    confidence = float(gate.get("confidence", 0.0))
    valid = bool(gate.get("valid", False)) and confidence >= 0.65

    return ValidateResponse(
        valid=valid,
        reason=str(gate.get("reason", "OK")),
        requiredQuestions=list(gate.get("requiredQuestions", []))[:6],
        confidence=confidence,
    )


@app.post("/api/generate", response_model=WorkItemDraft)
def generate(req: GenerateRequest):
    validation = validate(ValidateRequest(notesText=req.notesText))
    if not validation.valid:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Cannot generate a work item because the notes are unclear.",
                "reason": validation.reason,
                "requiredQuestions": validation.requiredQuestions,
                "confidence": validation.confidence,
            },
        )

    try:
        return generate_work_item_draft(
            notes_text=req.notesText,
            work_item_type=req.workItemType,
            process=req.process,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/workitems/create", response_model=CreateWorkItemResponse)
def create_workitem(req: CreateWorkItemRequest):
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
