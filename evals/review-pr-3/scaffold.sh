#!/usr/bin/env bash
set -euo pipefail
mkdir -p app worker tests/unit
cat > app/schemas.py <<'PY'
from typing import Optional
from pydantic import BaseModel


class ProfileResponse(BaseModel):
    user_id: str
    display_name: str
    avatar_url: Optional[str] = None
PY
cat > app/service.py <<'PY'
from .schemas import ProfileResponse


def build_profile(user_id: str, display_name: str, avatar_url: str | None) -> ProfileResponse:
    if avatar_url is not None and not avatar_url.startswith("https://"):
        raise ValueError("avatar_url must be https")
    return ProfileResponse(user_id=user_id, display_name=display_name, avatar_url=avatar_url)
PY
cat > app/router.py <<'PY'
from fastapi import APIRouter

from .schemas import ProfileResponse
from .service import build_profile

router = APIRouter()


@router.get("/profile/{user_id}")
async def get_profile(user_id: str) -> ProfileResponse:
    return build_profile(user_id, "placeholder", None)
PY
cat > worker/rebuild_profiles.py <<'PY'
from app.schemas import ProfileResponse

# Backfill job: rebuilds a profile from an old row that has no avatar yet.
def rebuild(user_id: str, display_name: str) -> ProfileResponse:
    return ProfileResponse(user_id=user_id, display_name=display_name)
PY
cat > tests/unit/test_service.py <<'PY'
from app.service import build_profile


def test_profile_without_avatar():
    p = build_profile("u1", "Ann", None)
    assert p.avatar_url is None
PY
git init -q
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "initial"
git branch main
cat > app/schemas.py <<'PY'
from pydantic import BaseModel


class ProfileResponse(BaseModel):
    user_id: str
    display_name: str
    avatar_url: str  # now required -- validation moved to the router
PY
cat > app/router.py <<'PY'
from fastapi import APIRouter, HTTPException

from .schemas import ProfileResponse
from .service import build_profile

router = APIRouter()


@router.get("/profile/{user_id}")
async def get_profile(user_id: str) -> ProfileResponse:
    avatar_url = "https://cdn.example.com/default.png"
    if not avatar_url.startswith("https://"):
        raise HTTPException(400, "avatar_url must be https")
    return build_profile(user_id, "placeholder", avatar_url)
PY
cat > app/service.py <<'PY'
from .schemas import ProfileResponse


def build_profile(user_id: str, display_name: str, avatar_url: str) -> ProfileResponse:
    return ProfileResponse(user_id=user_id, display_name=display_name, avatar_url=avatar_url)
PY
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "move avatar validation into the router, require avatar_url"
