def route_intent(text: str):

    text = text.lower()

    if "hora" in text:
        return "time"

    if "clima" in text:
        return "weather"

    return "unknown"


"""
==================================================
NOTA DE ARQUITECTURA:
Esto es un clasificador primitivo:

no usa ML
no usa embeddings
es deterministic routing

👉 base de todo sistema de agentes simples
==================================================
"""