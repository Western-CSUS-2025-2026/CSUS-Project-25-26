import hmac
import hashlib
import time
from fastapi import Request, HTTPException
from api.settings import get_settings

settings = get_settings()

WEBHOOK_SECRET = settings.TWELVE_LABS_WEBHOOK_SECRET


def verify_twelvelabs_signature(raw_body: bytes, signature_header: str) -> bytes:
    """Verify Twelve Labs webhook signature. Returns raw body if valid."""
    if not signature_header:
        raise HTTPException(status_code=400, detail="TL-Signature header is required")
    
    # Parse t and v1 from header
    parts = {}
    for part in signature_header.split(','):
        key, value = part.split("=", 1)
        parts[key] = value

    timestamp = parts.get("t")
    received_sig = parts.get("v1")

    if not timestamp or not received_sig:
        raise HTTPException(status_code=400, detail="Invalid TL-Signature header")

    if abs(time.time() - int(timestamp)) > 300:
        raise HTTPException(status_code=400, detail="Timestamp is too old")

    signed_payload = f"{timestamp}.{raw_body.decode()}"

    expected_sig = hmac.new(
        WEBHOOK_SECRET.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, received_sig):
        raise HTTPException(status_code=400, detail="Invalid TL-Signature header")

    return raw_body
    