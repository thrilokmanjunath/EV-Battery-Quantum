import re
import json
from datetime import datetime
from typing import Dict, Any

class TelemetryEvent:
    def __init__(self, level: str, module: str, message: str):
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.level = level
        self.module = module
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "module": self.module,
            "message": self.message
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class LogSanitizer:
    """
    Sanitizes raw worker logs to prevent exposure of sensitive quantum state vectors,
    proprietary battery formulas, or API keys.
    """
    SENSITIVE_PATTERNS = [
        re.compile(r"(?i)api_key[\s:=]+[a-zA-Z0-9_\-]+"),
        re.compile(r"Traceback \(most recent call last\):.*", re.DOTALL),
        re.compile(r"Statevector\(\[.*\]\)", re.DOTALL),  # Hide raw quantum states
        re.compile(r"(?i)(NMC|LFP|Solid-State).*?(formula|ratio)[\s:=]+[\d\.]+"), # Hide chemistry ratios
    ]

    @classmethod
    def sanitize(cls, raw_message: str, level: str = "INFO", module: str = "QAOA") -> TelemetryEvent:
        clean_message = raw_message

        # Strip tracebacks
        if "Traceback" in clean_message:
            clean_message = "Internal processing error occurred. Traceback suppressed for security."
            level = "ERROR"
            
        # Regex redactions
        for pattern in cls.SENSITIVE_PATTERNS:
            clean_message = pattern.sub("[REDACTED]", clean_message)

        return TelemetryEvent(level=level, module=module, message=clean_message)

# Example interceptor function for Celery
def process_celery_log(raw_message: str) -> str:
    event = LogSanitizer.sanitize(raw_message, module="CeleryWorker")
    return event.to_json()
