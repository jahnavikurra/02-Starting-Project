import base64
import json
from typing import Any, Dict, List

import requests

from src.utils.config import settings


def _auth_header_from_pat(pat: str) -> str:
    token = base64.b64encode(f":{pat}".encode("utf-8")).decode("utf-8")
    return f"Basic {token}"


def create_work_item(
    *,
    title: str,
    description_md: str,
    acceptance_criteria: List[str],
    work_item_type: str,  # "PBI" | "Bug" | "Task"
) -> Dict[str, Any]:
    if not settings.ADO_ORG_URL:
        raise RuntimeError("ADO_ORG_URL is missing")
    if not settings.ADO_PROJECT:
        raise RuntimeError("ADO_PROJECT is missing")
    if not settings.ADO_PAT:
        raise RuntimeError("ADO_PAT is missing (store as Container App secretref)")

    wit = work_item_type
    if work_item_type == "PBI":
        wit = "Product Backlog Item"  # Scrum process default name

    url = (
        f"{settings.ADO_ORG_URL}/{settings.ADO_PROJECT}"
        f"/_apis/wit/workitems/${wit}?api-version=7.1-preview.3"
    )

    ac_text = "\n".join([f"- {x}" for x in acceptance_criteria]) if acceptance_criteria else ""

    patch_ops = [
        {"op": "add", "path": "/fields/System.Title", "value": title},
        {"op": "add", "path": "/fields/System.Description", "value": description_md},
    ]

    if ac_text:
        patch_ops.append(
            {"op": "add", "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria", "value": ac_text}
        )

    headers = {
        "Content-Type": "application/json-patch+json",
        "Authorization": _auth_header_from_pat(settings.ADO_PAT),
    }

    resp = requests.post(url, headers=headers, data=json.dumps(patch_ops), timeout=30)
    if resp.status_code >= 400:
        raise RuntimeError(f"ADO create failed {resp.status_code}: {resp.text}")

    return resp.json()
