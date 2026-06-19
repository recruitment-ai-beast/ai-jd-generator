"""
Prompt templates for JD generation.
All prompt logic lives here — isolated from business logic.
"""

SYSTEM_PROMPT = """\
You are an expert HR consultant and recruitment copywriter.

Your goal is to create ATS-friendly, inclusive, high-converting
job descriptions that attract qualified candidates while
reducing irrelevant applications.

Rules:
- Avoid corporate jargon
- Use inclusive language
- Use specific requirements
- Separate must-have and nice-to-have skills
- Prefer action verbs for responsibilities
- Avoid vague filler
- Prioritize readability
- ATS optimized
- Professional but human\
"""

JD_GENERATION_PROMPT = """\
Generate a complete, professional job description using the inputs below.

Job Title: {job_title}
Key Responsibilities: {responsibilities}
Required Skills: {skills}
Experience Level: {experience_level}
Company Culture: {company_culture}
Tone: {tone}
Target Word Count: {word_count}

Return EXACTLY in this format — no extra commentary:

## Optimized Job Title
[improved title]

## Company Overview
[2-3 sentence company summary]

## Role Overview
[2-3 sentence role summary]

## Key Responsibilities
[bullet points with action verbs]

## Skills Required
### Must Have
[bullet points]

### Nice To Have
[bullet points]

## Salary Range
[realistic range with disclaimer]

## Benefits
[bullet points]

## How To Apply
[strong CTA]

## SEO Keywords
[comma-separated keywords for job boards]

## ATS Score
[score out of 100 with one-line reasoning]

## Bias Analysis
[flag any gender-coded or exclusionary language, or state "No bias detected."]\
"""

VARIATION_PROMPT = """\
Generate {variation_label} of this job description with a different angle:

Original inputs:
Job Title: {job_title}
Responsibilities: {responsibilities}
Skills: {skills}
Experience: {experience_level}
Tone: {tone}

Make it distinct — different opening, different emphasis, same core requirements.
Label it clearly as {variation_label}.\
"""
