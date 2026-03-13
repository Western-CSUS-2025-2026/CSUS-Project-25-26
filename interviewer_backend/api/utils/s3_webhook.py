import base64
import logging
import urllib.request
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
from functools import lru_cache

from urllib.parse import urlparse

from api.exceptions import SNSVerificationFailed

logger = logging.getLogger(__name__)


@lru_cache(maxsize=128)
def fetch_cert(cert_url: str) -> bytes:
    """Fetch and cache the signing cert from AWS."""
    # Only trust AWS domains; reject missing/malformed URLs
    parsed = urlparse(cert_url)
    if not parsed.hostname:
        raise SNSVerificationFailed(f"Missing or invalid cert URL hostname: {cert_url!r}")
    if not parsed.hostname.endswith(".amazonaws.com"):
        raise SNSVerificationFailed(f"Untrusted cert URL: {cert_url}")

    with urllib.request.urlopen(cert_url) as response:
        return response.read()


def build_signature_string(payload: dict) -> str:
    """Reconstruct the exact string AWS signed. Field order is strict."""
    if payload["Type"] == "Notification":
        fields = ["Message", "MessageId", "Subject", "Timestamp", "TopicArn", "Type"]
    else:
        # SubscriptionConfirmation / UnsubscribeConfirmation
        fields = ["Message", "MessageId", "SubscribeURL", "Timestamp", "Token", "TopicArn", "Type"]

    # Build string: "Key\nValue\n" per field (trailing newline per boto3#2508 / production gists).
    parts = []
    for field in fields:
        if field in payload:
            val = payload[field]
            if not isinstance(val, str):
                val = str(val)
            parts.append(f"{field}\n{val}\n")
    result = "".join(parts)
    # DEBUG: log length + preview (Message can be huge; avoid full dump)
    preview = result[:200] + "..." if len(result) > 200 else result
    logger.info("SNS string-to-sign len=%d preview=%r", len(result), preview)
    return result


def verify_sns_signature(payload: dict) -> None:
    """
    Verify SNS message signature.
    Raises SNSVerificationFailed if invalid; caller should return 403.
    """

    cert_pem = fetch_cert(payload["SigningCertURL"])
    cert = load_pem_x509_certificate(cert_pem)
    public_key = cert.public_key()

    signature = base64.b64decode(payload["Signature"])
    message = build_signature_string(payload).encode("utf-8")

    hash_algo = hashes.SHA256() if payload.get("SignatureVersion") == "2" else hashes.SHA1()

    try:
        public_key.verify(signature, message, padding.PKCS1v15(), hash_algo)
    except InvalidSignature as e:
        logger.warning(
            "SNS signature verification failed: SignatureVersion=%s cert_url=%s msg_len=%d",
            payload.get("SignatureVersion"),
            payload.get("SigningCertURL"),
            len(message),
        )
        raise SNSVerificationFailed(f"Invalid SNS signature: {e!s}") from e
