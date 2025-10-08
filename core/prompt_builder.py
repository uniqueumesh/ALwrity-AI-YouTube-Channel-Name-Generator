"""
Prompt building logic for AI name generation.
"""

def build_youtube_prompt(description, language, tone, variants):
    """Builds a stricter, higher-quality prompt for brandable YouTube names.

    The prompt enforces: exact count, strict JSON output, language/script control,
    anti-generic constraints, and brandability/variety guidance.
    """

    return f"""
You are a brand-naming assistant. Generate exactly {variants} unique YouTube channel names.

Context:
- Channel description: "{description}"
- Target language: {language}. Output must be ONLY in this language (and its native script if applicable).
- Tone/style: {tone}

Hard constraints (must all be satisfied):
- Count: exactly {variants} names.
- Output format: names only, no explanations, no numbering, no extra text.
- Length: 2–4 words; 8–25 characters total after trimming.
- Case: Title Case (Capitalize Each Word); not ALL CAPS; no trailing/leading spaces.
- Characters: letters and spaces only. Disallow digits, punctuation, symbols, emojis, hyphens and underscores.
- Content: brandable, specific, memorable; clearly tied to the description’s domain vocabulary.
- Avoid generic fillers: do not overuse or rely on words like "Channel", "Tube", "TV", "Official", "Media", "Studio", "Hub". Permit at most one name that uses one of those as a tasteful suffix.
- Uniqueness: no duplicates or near-duplicates; vary structure (e.g., compound, metaphor, subtle alliteration, contrast pairs) without clichés.
- Safety: avoid trademarks/brand names, personal names, or sensitive content.

Validation you must perform BEFORE responding:
- The JSON array length is {variants}.
- Every item satisfies ALL constraints.
- All names are in {language} and correct script.

Output (STRICT): return ONLY this JSON (no prose, no markdown fences):
{{"names": ["Name 1", "Name 2", "Name 3"]}}
"""
