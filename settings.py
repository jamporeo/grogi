# settings.py
import os

# Rutas base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Configuración de pantalla
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colores (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)
LIGHT_YELLOW = (255, 255, 200)

# Fuente predeterminada
DEFAULT_FONT = os.path.join(FONTS_DIR, "pixel_font.ttf")
if not os.path.exists(DEFAULT_FONT):
    DEFAULT_FONT = None  # Usar fuente predeterminada del sistema