class PrimaryModelError(Exception):
    """The primary Gemini model failed; fallback may be offered."""
    pass


class FallbackModelError(Exception):
    """Both the primary attempt and fallback attempt failed."""
    pass
