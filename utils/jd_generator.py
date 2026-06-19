"""
Core JD generation logic.
LangChain + Groq integration lives here.
"""

import logging
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from utils.prompts import SYSTEM_PROMPT, JD_GENERATION_PROMPT, VARIATION_PROMPT

logger = logging.getLogger(__name__)


def build_model(api_key: str) -> ChatGroq:
    """Initialise Groq LLM."""
    return ChatGroq(
        model="gemma2-9b-it",
        temperature=0.7,
        max_tokens=2000,
        api_key=api_key
    )


def generate_jd(
    api_key: str,
    job_title: str,
    responsibilities: str,
    skills: str,
    experience_level: str,
    company_culture: str,
    tone: str,
    word_count: int
) -> Optional[str]:
    """
    Generate a single job description.
    Returns generated text or None on failure.
    """
    try:
        model = build_model(api_key)

        prompt = JD_GENERATION_PROMPT.format(
            job_title=job_title,
            responsibilities=responsibilities,
            skills=skills,
            experience_level=experience_level,
            company_culture=company_culture or "Not specified",
            tone=tone,
            word_count=word_count
        )

        response = model.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ])

        return response.content

    except Exception as e:
        logger.error(f"JD generation failed: {e}")
        return None


def generate_variations(
    api_key: str,
    job_title: str,
    responsibilities: str,
    skills: str,
    experience_level: str,
    tone: str
) -> dict:
    """
    Generate 3 JD variations for A/B testing.
    Returns dict with Version A, B, C.
    """
    model = build_model(api_key)
    variations = {}

    for label in ["Version A", "Version B", "Version C"]:
        try:
            prompt = VARIATION_PROMPT.format(
                variation_label=label,
                job_title=job_title,
                responsibilities=responsibilities,
                skills=skills,
                experience_level=experience_level,
                tone=tone
            )

            response = model.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ])

            variations[label] = response.content

        except Exception as e:
            logger.error(f"Variation {label} failed: {e}")
            variations[label] = f"Could not generate {label}."

    return variations
