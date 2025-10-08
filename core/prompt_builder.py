"""
Prompt building logic for AI name generation.
"""

def build_youtube_prompt(description, language, tone, variants):
    """Build simple prompt to avoid safety filtering"""
    
    return f"""Create {variants} YouTube channel names for: {description}

Style: {tone}
Language: {language}

Rules:
- 2-4 words each
- 8-25 characters total
- No numbers or special characters
- Brandable and memorable

Return as JSON: {{"names": ["Name1", "Name2", "Name3"]}}"""
