#!/usr/bin/env bash
set -euo pipefail
mkdir -p app
cat > app/orders.py <<'PY'
def create_order(session, customer_id: int, total: int) -> int:
    order_id = session.execute(
        "INSERT INTO orders (customer_id, total) VALUES (:c, :t) RETURNING id",
        {"c": customer_id, "t": total},
    ).scalar_one()
    session.commit()
    return order_id
PY
git init -q
git -c user.email=eval@example.com -c user.name=eval commit -q --allow-empty -m "initial"
git branch main
cat > app/orders.py <<'PY'
async def create_order(session, customer_id: int, total: int) -> int:
    try:
        result = session.execute(
            "INSERT INTO orders (customer_id, total) VALUES (:c, :t) RETURNING id",
            {"c": customer_id, "t": total},
        )
        order_id = result.scalar_one()
        session.commit()
        return order_id
    except Exception:
        # No rollback here: the session keeps the failed statement in its
        # transaction, and the next call on this pooled connection inherits
        # an aborted transaction.
        raise
PY
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "make create_order async"
