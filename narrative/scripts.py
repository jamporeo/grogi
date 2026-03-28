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
        "text": "Pero para lograrlo, necesitarás tres ingredientes sagrados: Papa, Carne molida y Queso."
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
    "correct": 1,
    "success_message": "¡Enhorabuena! ¡Has conseguido la bolsa de papas!",
    "failure_message": "Mmm... esa no es la verdadera papa sagrada. Inténtalo de nuevo."
}

NARRATOR_VOICES = {
    "papa": "¡Enhorabuena! ¡Has conseguido la bolsa de papas!",
    "carne": "¡Bien hecho! La carne molida está lista.",
    "queso": "¡El queso está fresco y listo para el pastel!",
    "final": "Muy bien, Zoóloga. Ahora son 50 pasteles más para eliminar la corrupción."
}

# --- Finales ---
GOOD_ENDING_DIALOGUE = [
    {
        "speaker": "Narrador",
        "text": "Narrador: El pastel de papa sale perfecto y las tres se sirven una buena porción."
    },
    {
        "speaker": "Mecánica",
        "text": "Mecánica: ¡Amiga, esto está increíble! Hace años que no comía uno así."
    },
    {
        "speaker": "Steampunker",
        "text": "Steampunker: Estoy tan llena que no me puedo mover… literal."
    },
    {
        "speaker": "Zoóloga",
        "text": "Zoóloga: Jajaja, me alegra que les haya gustado tanto."
    },
    {
        "speaker": "Narrador",
        "text": "Narrador: Después de comer, charlan de que hace mucho no se veían y se quedan tiradas, incapaces de moverse del empacho."
    }
]

BAD_ENDING_DIALOGUE = [
    {
        "speaker": "Narrador",
        "text": "Narrador: Pero la Zoóloga cambia la cara de golpe."
    },
    {
        "speaker": "Zoóloga",
        "text": "Zoóloga: Ay… creo que la cagué con los ingredientes… y encima se lo di todo a mi ‘abrevadero de dinero’."
    },
    {
        "speaker": "Mecánica",
        "text": "Mecánica: ¿Cómo? ¿Entonces no podemos comer?"
    },
    {
        "speaker": "Zoóloga",
        "text": "Zoóloga: Perdón… posta…"
    },
    {
        "speaker": "Mecánica",
        "text": "Mecánica: Bueno, ya fue… cerca hay un restaurante barato. ¿Vamos?"
    },
    {
        "speaker": "Steampunker",
        "text": "Steampunker: Y… no nos queda otra."
    },
    {
        "speaker": "Zoóloga",
        "text": "Zoóloga: Perdón chicas… la próxima de verdad lo hago bien."
    },
    {
        "speaker": "Narrador",
        "text": "Narrador: Las tres abandonan el plan original y terminan comiendo en un restaurante barato a la vuelta."
    }
]