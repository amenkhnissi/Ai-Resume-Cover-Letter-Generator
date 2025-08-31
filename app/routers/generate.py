from fastapi import APIRouter, HTTPException
from ..schemas import GenerateRequest, GenerateResponse
from ..prompts import (
    COVER_LETTER_SYSTEM, RESUME_BULLETS_SYSTEM,
    COVER_LETTER_USER_TEMPLATE, RESUME_BULLETS_USER_TEMPLATE,)
from ..openai_client import get_client
import re

router = APIRouter(prefix="/generate", tags=["generate"])

SAFE_MIN = 50

# basic prompt hygiene
FORBIDDEN = re.compile(
    r"(password|ssn|social\s*security|credit\s*card|api\s*key)", re.I)


def sanitize(text: str) -> str:
    if FORBIDDEN.search(text or ""):
        raise HTTPException(400, detail="Sensitive secrets detected in input.")
    return text.strip()


@router.post("/all", response_model=GenerateResponse)
async def generate_all(req: GenerateRequest):
    resume = sanitize(req.resume_text)
    jd = sanitize(req.job_description)
    if len(resume) < SAFE_MIN or len(jd) < SAFE_MIN:
        raise HTTPException(
            400, detail="Resume and JD must be at least 50 chars.")

    client = get_client()

    # Cover letter
    cl_user = (
        COVER_LETTER_USER_TEMPLATE
        .replace("{{RESUME}}", resume)
        .replace("{{JD}}", jd)
        .replace("{{TONE}}", req.tone_hint or "balanced professional")
    )

    cl = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": COVER_LETTER_SYSTEM},
            {"role": "user", "content": cl_user},
        ],
        temperature=0.3,
    )
    cover_letter = cl.choices[0].message.content

    # Resume bullets
    rb_user = (
        RESUME_BULLETS_USER_TEMPLATE
        .replace("{{RESUME}}", resume)
        .replace("{{JD}}", jd)
    )

    rb = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": RESUME_BULLETS_SYSTEM},
            {"role": "user", "content": rb_user},
        ],
        temperature=0.25,
    )
    bullets = rb.choices[0].message.content
    return GenerateResponse(cover_letter=cover_letter, bullets=bullets)
