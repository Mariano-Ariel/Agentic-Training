from .router import route_intent
from .tools import get_time, get_weather


def run_agent(user_input: str):

    intent = route_intent(user_input)

    if intent == "time":
        return get_time()

    if intent == "weather":
        return get_weather()

    return "No se pudo resolver la intención"


"""
==================================================
INPUT → clasificación → ejecución → OUTPUT
==================================================
"""
