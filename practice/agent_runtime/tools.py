from datetime import datetime


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def get_weather():
    return "Mock: 22°C soleado (sin API integrada)"

"""
==================================================
Esto es importante: las tools son la parte del agente que interactúa con el mundo real.

tools = “interacciones con el mundo”
APIs
base de datos
sistema operativo
etc.

Por ahora mock.
==================================================
"""