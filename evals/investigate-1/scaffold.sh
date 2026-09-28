#!/usr/bin/env bash
set -euo pipefail
mkdir -p src logs
cat > src/ws_server.py <<'PY'
import asyncio
import logging

logger = logging.getLogger("ws")
HEARTBEAT_INTERVAL = 15  # seconds


async def handle_connection(ws):
    """Serve one WebSocket connection until the client disconnects."""
    try:
        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=HEARTBEAT_INTERVAL)
            except asyncio.TimeoutError:
                # Intended as a heartbeat check, not a real error.
                await ws.ping()
                continue
            await handle_message(ws, msg)
    except Exception as exc:
        # Any exception -- including the heartbeat TimeoutError from a
        # slow client that just hasn't sent anything in 15s -- lands
        # here and the connection is torn down.
        logger.info("closing connection: %s", exc)
        await ws.close(code=1011)


async def handle_message(ws, msg):
    await ws.send(msg)
PY
cat > logs/app.log <<'LOG'
2026-09-01T10:00:00Z INFO ws: connection opened client=203.0.113.5
2026-09-01T10:00:15Z INFO ws: closing connection: (TimeoutError())
2026-09-01T10:00:15Z INFO ws: connection closed code=1011
2026-09-01T10:04:02Z INFO ws: connection opened client=203.0.113.9
2026-09-01T10:04:17Z INFO ws: closing connection: (TimeoutError())
2026-09-01T10:04:17Z INFO ws: connection closed code=1011
2026-09-01T10:11:40Z INFO ws: connection opened client=203.0.113.5
2026-09-01T10:11:55Z INFO ws: closing connection: (TimeoutError())
2026-09-01T10:11:55Z INFO ws: connection closed code=1011
LOG
git init -q
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -q -m "initial"
