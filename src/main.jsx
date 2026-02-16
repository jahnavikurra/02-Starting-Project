from fastapi import FastAPI, HTTPException

from src.models.schemas import (
    GenerateRequest,
    WorkItemDraft,
    ValidateRequest,
    ValidateResponse,
)
from src.utils.validator import validate_notes_text
from src.services.llm_gate import gate_validate_notes
from src.services.llm import generate_work_item_draft

app = FastAPI(title="AI WorkItems Backend")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/validate", response_model=ValidateResponse)
def validate(req: ValidateRequest):
    # 1) Deterministic check
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

    # 2) LLM gate check (Managed Identity)
    gate = gate_validate_notes(req.notesText)

    return ValidateResponse(
        valid=bool(gate.get("valid", False)) and float(gate.get("confidence", 0.0)) >= 0.65,
        reason=str(gate.get("reason", "OK")),
        requiredQuestions=list(gate.get("requiredQuestions", []))[:6],
        confidence=float(gate.get("confidence", 0.0)),
    )


@app.post("/api/generate", response_model=WorkItemDraft)
def generate(req: GenerateRequest):
    # Reuse validate endpoint logic
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
