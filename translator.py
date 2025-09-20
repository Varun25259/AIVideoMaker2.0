def translate_text(text, target_langs=['en']):
    # Placeholder translation function.
    translations = {}
    for lang in target_langs:
        translations[lang] = '[Translated ' + lang + '] ' + text[:500]
    return translations
