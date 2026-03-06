import hashlib
import hmac
import logging
import time

from api.exceptions import WebhookVerificationFailed
from api.settings import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

WEBHOOK_SECRET = settings.TWELVE_LABS_WEBHOOK_SECRET


def verify_twelvelabs_signature(raw_body: bytes, signature_header: str) -> bytes:
    """Verify Twelve Labs webhook signature. Returns raw body if valid."""

    if not signature_header or not WEBHOOK_SECRET:
        raise WebhookVerificationFailed()

    parts = {}
    for part in signature_header.split(","):
        key, value = part.split("=", 1)
        parts[key] = value

    timestamp = parts.get("t")
    received_sig = parts.get("v1")

    if not timestamp or not received_sig:
        raise WebhookVerificationFailed()

    if abs(time.time() - int(timestamp)) > 300:
        raise WebhookVerificationFailed()

    signed_payload = f"{timestamp}.{raw_body.decode()}"

    expected_sig = hmac.new(
        WEBHOOK_SECRET.encode(),
        signed_payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, received_sig):
        raise WebhookVerificationFailed()

    return raw_body

