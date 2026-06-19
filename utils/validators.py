"""
Input validation layer.
All validation logic isolated here.
Returns (is_valid: bool, error_message: str).
"""

from typing import Tuple


def validate_inputs(
    job_title: str,
    responsibilities: str,
    skills: str,
    experience_level: str
) -> Tuple[bool, str]:
    """Validate all required form inputs."""

    if not job_title.strip():
        return False, "Please enter a job title to continue."

    if len(job_title.strip()) < 3:
        return False, "Job title must be at least 3 characters."

    if not responsibilities.strip():
        return False, "Add at least one responsibility before generating."

    if len(responsibilities.strip()) < 20:
        return False, "Please provide more detail in the responsibilities field."

    if not skills.strip():
        return False, "Please add at least one required skill."

    if not experience_level:
        return False, "Please select an experience level."

    return True, ""


def validate_api_key(api_key: str) -> Tuple[bool, str]:
    """Validate Groq API key format."""
    if not api_key:
        return False, "GROQ_API_KEY not found. Check your environment variables."
    if not api_key.startswith("gsk_"):
        return False, "Invalid API key format."
    return True, ""
