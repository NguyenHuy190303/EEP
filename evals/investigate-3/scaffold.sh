#!/usr/bin/env bash
set -euo pipefail
mkdir -p app tests/unit migrations config
cat > app/models.py <<'PY'
class Customer:
    id: int
    name: str


class Order:
    id: int
    customer_id: int  # FK -> Customer.id
PY
cat > app/events.py <<'PY'
import json


async def publish_order_event(order_id: int, customer_id: int) -> None:
    """Publish to 'orders' topic: {"order_id": int, "customer_id": int}."""
    payload = json.dumps({"order_id": order_id, "customer_id": customer_id})
    ...
PY
cat > migrations/0007_orders.sql <<'SQL'
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id)
);
SQL
cat > tests/unit/test_orders.py <<'PY'
from app.models import Customer, Order


def test_order_links_to_customer():
    c = Customer()
    c.id = 42
    o = Order()
    o.customer_id = 42
    assert o.customer_id == c.id
PY
cat > config/feature_flags.yaml <<'YAML'
# customer_id here mirrors app/models.py::Customer.id and must stay in sync
legacy_customer_id_format: int
YAML
git init -q
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "initial"
