#!/usr/bin/env bash
set -euo pipefail
mkdir -p app
cat > app/config.py <<'PY'
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    payments_api_url: str
    payments_api_timeout_s: int = 5


settings = Settings()
PY
cat > app/payments.py <<'PY'
import httpx

from .config import settings


def charge(customer_id: str, amount_cents: int) -> dict:
    resp = httpx.post(
        f"{settings.payments_api_url}/charge",
        json={"customer_id": customer_id, "amount_cents": amount_cents},
        timeout=settings.payments_api_timeout_s,
    )
    resp.raise_for_status()
    return resp.json()
PY
git init -q
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "initial"
cat > app/payments.py <<'PY'
import os
import time

import httpx

from .config import settings

PAYMENTS_STRICT_MODE = os.environ.get("PAYMENTS_STRICT_MODE")


def charge(customer_id: str, amount_cents: int) -> dict:
    for attempt in range(5):
        try:
            resp = httpx.post(
                f"{settings.payments_api_url}/charge",
                json={"customer_id": customer_id, "amount_cents": amount_cents},
                timeout=settings.payments_api_timeout_s,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception:
            time.sleep(0.1)
    raise RuntimeError("payment failed after retries")
PY
# Left as an uncommitted working-tree change -- this is a local diff, not yet a commit.
