KANNADA_TO_ENGLISH = {
    "ಬೆಂಗಳೂರಿನಲ್ಲಿ ಸೈಬರ್ ಅಪರಾಧ ಪ್ರಕರಣಗಳ ಮುನ್ಸೂಚನೆ": "Forecast cyber crime cases in Bengaluru",
    "ಅಪರಾಧ ದಾಖಲೆಗಳು": "crime records",
    "ಹೋರಾಟ": "Assault",
    "ಕಳ್ಳತನ": "Theft",
    "ಮಾದಕ ದ್ರವ್ಯಗಳು": "Narcotics",
    "ಮಹಿಳೆಯರ ಮೇಲಿನ ದೌರ್ಜನ್ಯ": "Crimes Against Women"
}

def translate_kannada_to_english(query: str) -> str:
    """
    Translates Kannada input queries to English.
    """
    for kan, eng in KANNADA_TO_ENGLISH.items():
        if kan in query:
            return query.replace(kan, eng)
    return query

def translate_english_to_kannada(text: str) -> str:
    """
    Translates English responses back to Kannada.
    """
    # Simple dictionary replacement for demo text
    replacements = {
        "Found": "ಕಂಡುಬಂದಿದೆ",
        "cases": "ಪ್ರಕರಣಗಳು",
        "Based on database records": "ಡೇಟಾಬೇಸ್ ದಾಖಲೆಗಳ ಆಧಾರದ ಮೇಲೆ",
        "in": "ನಲ್ಲಿ",
        "solved": "ಪರಿಹರಿಸಲಾಗಿದೆ"
    }
    for eng, kan in replacements.items():
        text = text.replace(eng, kan)
    return text
