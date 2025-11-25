# narrative/scripts.py

INTRO_DIALOGUE = [
    {
        "speaker": "Narrador",
        "text": "En un mundo en peligro por la maldad de la Corrupción, solo un plato puede salvarnos..."
    },
    {
        "speaker": "Zoóloga",
        "text": "¡Yo, la Zoóloga de Terraria, acepto esta misión! Haré el mejor pastel de papa del universo."
    },
    {
        "speaker": "Narrador",
        "text": "Pero para lograrlo, necesitarás tres ingredientes sagrados: Papa, Carne molida y Verduras."
    },
    {
        "speaker": "Zoóloga",
        "text": "¡No hay tiempo que perder! ¡A buscarlos!"
    }
]

# --- Acertijo de la Papa ---
PAPA_RIDDLE = {
    "question": "Soy redonda, crezco bajo tierra y soy esencial para el pastel que salvará al mundo.\n¿Quién soy?",
    "options": ["A) Zanahoria", "B) Papa", "C) Cebolla"],
    "correct": 1,  # índice de la respuesta correcta (B)
    "success_message": "¡Enhorabuena! ¡Has conseguido la bolsa de papas!",
    "failure_message": "Mmm... esa no es la verdadera papa sagrada. Inténtalo de nuevo."
}

NARRATOR_VOICES = {
    "papa": "¡Enhorabuena! ¡Has conseguido la bolsa de papas!",
    "carne": "¡Bien hecho! La carne molida está lista.",
    "verduras": "Las verduras están frescas y listas para usar.",
    "final": "Muy bien, Zoóloga. Ahora son 50 pasteles más para eliminar la corrupción."
}