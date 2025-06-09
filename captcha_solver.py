"""Placeholder captcha solving helper."""

import os


def solve_captcha(image_path: str) -> str:
    """Return solved captcha text using 2captcha API if key provided."""
    api_key = os.getenv('CAPTCHA_API_KEY')
    if not api_key:
        raise RuntimeError('CAPTCHA_API_KEY not set')
    # In a real implementation, send HTTP request to 2captcha or similar.
    # Here we return a fake result for demonstration.
    return 'solved-text'
