#!/usr/bin/env bash
set -euo pipefail
mkdir -p app
cat > app/schemas.py <<'PY'
from pydantic import BaseModel


class SignupRequest(BaseModel):
    tenant_id: str
    email: str
PY
cat > app/router.py <<'PY'
from fastapi import APIRouter

from .schemas import SignupRequest
from .db import insert_signup
from .events import publish_signup_event

router = APIRouter()


@router.post("/signup")
async def signup(body: SignupRequest):
    row_id = await insert_signup(tenant_id=body.tenant_id, email=body.email)
    await publish_signup_event(tenant_id=body.tenant_id, signup_id=row_id)
    return {"id": row_id}
PY
cat > app/db.py <<'PY'
async def insert_signup(tenant_id: str, email: str) -> int:
    """INSERT INTO signups (tenant_id, email) VALUES ($1, $2) RETURNING id."""
    ...
PY
cat > app/events.py <<'PY'
import json


async def publish_signup_event(tenant_id: str, signup_id: int) -> None:
    """Publish to the 'signups' Kafka topic as JSON: {"tenant_id": ..., "signup_id": ...}."""
    payload = json.dumps({"tenant_id": tenant_id, "signup_id": signup_id})
    ...
PY
git init -q
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "initial"
