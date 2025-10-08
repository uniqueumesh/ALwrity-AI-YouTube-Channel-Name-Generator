"""
Fallback name generation when API fails.
"""

import orjson

def generate_fallback_names(description, variants):
    """Generate fallback names when API fails"""
    import random
    
    # Extract keywords from description
    words = description.lower().split()
    keywords = [w for w in words if len(w) > 3 and w not in ['the', 'and', 'for', 'with', 'from', 'this', 'that', 'about', 'your', 'channel', 'videos', 'content']]
    
    # Enhanced name templates based on common YouTube niches
    templates = [
        "{keyword} {suffix}",
        "{prefix} {keyword}",
        "{keyword} {keyword2}",
        "{prefix} {keyword} {suffix}",
        "{keyword} {suffix} {suffix2}",
        "{keyword}TV",
        "{keyword}Tube",
        "{keyword}Channel"
    ]
    
    # More relevant prefixes and suffixes
    prefixes = ["Pro", "Elite", "Master", "Prime", "Ultra", "Super", "Max", "Top", "Best", "Great"]
    suffixes = ["Hub", "Zone", "Lab", "Studio", "Academy", "Works", "Pro", "Elite", "TV", "Tube", "Channel", "Media", "Content"]
    
    # Niche-specific suggestions
    niche_suggestions = {
        'cook': ['Kitchen', 'Chef', 'Taste', 'Food', 'Recipe'],
        'tech': ['Tech', 'Code', 'Dev', 'Digital', 'Cyber'],
        'fitness': ['Fit', 'Strong', 'Health', 'Gym', 'Workout'],
        'education': ['Learn', 'Study', 'Academy', 'School', 'Edu'],
        'gaming': ['Game', 'Play', 'Gamer', 'Arcade', 'Quest'],
        'music': ['Music', 'Sound', 'Audio', 'Beat', 'Rhythm'],
        'art': ['Art', 'Creative', 'Design', 'Studio', 'Canvas'],
        'travel': ['Travel', 'Journey', 'Adventure', 'Explore', 'Wander']
    }
    
    # Add niche-specific keywords
    for word in keywords:
        for niche, suggestions in niche_suggestions.items():
            if niche in word.lower():
                keywords.extend(suggestions)
                break
    
    names = []
    used_names = set()
    
    for i in range(variants):
        attempts = 0
        while attempts < 15:
            template = random.choice(templates)
            
            if "{keyword}" in template:
                keyword = random.choice(keywords) if keywords else "Channel"
            else:
                keyword = random.choice(keywords) if keywords else "Channel"
                
            if "{keyword2}" in template:
                keyword2 = random.choice(keywords) if len(keywords) > 1 else "Hub"
            else:
                keyword2 = "Hub"
                
            if "{prefix}" in template:
                prefix = random.choice(prefixes)
            else:
                prefix = "Pro"
                
            if "{suffix}" in template:
                suffix = random.choice(suffixes)
            else:
                suffix = "Hub"
                
            if "{suffix2}" in template:
                suffix2 = random.choice(suffixes)
            else:
                suffix2 = "Pro"
            
            name = template.format(
                keyword=keyword.title(),
                keyword2=keyword2.title(),
                prefix=prefix,
                suffix=suffix,
                suffix2=suffix2
            )
            
            # Clean up the name
            name = name.replace("  ", " ").strip()
            if 8 <= len(name) <= 25 and name not in used_names:
                names.append(name)
                used_names.add(name)
                break
            attempts += 1
    
    # If we don't have enough names, add some generic but relevant ones
    while len(names) < variants:
        generic_names = [
            "Channel Pro", "Content Hub", "Video Zone", "Media Lab", "Creative Studio",
            "Digital Academy", "Video Works", "Content Pro", "Media Hub", "Video Lab",
            "Channel Elite", "Content Zone", "Video Hub", "Media Pro", "Creative Lab"
        ]
        for gen_name in generic_names:
            if gen_name not in used_names and len(names) < variants:
                names.append(gen_name)
                used_names.add(gen_name)
    
    return f'{{"names": {orjson.dumps(names).decode()}}}'
