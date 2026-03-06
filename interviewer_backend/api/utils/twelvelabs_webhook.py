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
    logger.info("TL webhook: secret configured=%s", WEBHOOK_SECRET is not None)
    logger.info("TL webhook: signature_header=%s", signature_header)

    if not WEBHOOK_SECRET:
        logger.warning("TL webhook: no secret configured, skipping verification")
        return raw_body

    if not signature_header:
        logger.error("TL webhook: missing TL-Signature header")
        raise WebhookVerificationFailed("TL-Signature header is required")

    parts = {}
    for part in signature_header.split(","):
        key, value = part.split("=", 1)
        parts[key] = value

    timestamp = parts.get("t")
    received_sig = parts.get("v1")
    logger.info("TL webhook: timestamp=%s, received_sig=%s", timestamp, received_sig)

    if not timestamp or not received_sig:
        logger.error("TL webhook: could not parse t or v1 from header")
        raise WebhookVerificationFailed("Invalid TL-Signature header")

    age = abs(time.time() - int(timestamp))
    if age > 300:
        logger.error("TL webhook: timestamp too old, age=%ss", age)
        raise WebhookVerificationFailed("Timestamp is too old")

    signed_payload = f"{timestamp}.{raw_body.decode()}"

    expected_sig = hmac.new(
        WEBHOOK_SECRET.encode(),
        signed_payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, received_sig):
        logger.error("TL webhook: signature mismatch expected=%s received=%s", expected_sig, received_sig)
        raise WebhookVerificationFailed("Signature mismatch")

    logger.info("TL webhook: signature verified OK")
    return raw_body
