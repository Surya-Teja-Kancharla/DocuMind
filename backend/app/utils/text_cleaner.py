import re

def normalize_text(text: str) -> str:
    """
    Fix duplicated-character artifacts from bad PDF extraction.
    Example: 'BBaasseedd' -> 'Based'
    """

    # Collapse duplicated characters: aa -> a, BB -> B
    text = re.sub(r'(.)\1+', r'\1', text)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
