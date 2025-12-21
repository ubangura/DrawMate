"""DrawMate configuration constants"""
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Directories

# Project root directory (DrawMate/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

ASSET_DIR = PROJECT_ROOT / "assets"
DATA_DIR = PROJECT_ROOT / "data"
DATA_ASSET_DIR = DATA_DIR / "assets"
LOG_DIR = DATA_DIR / "logs"
GCODE_DIR = DATA_DIR / "gcode"
CONFIG_DIR = PROJECT_ROOT / "config"

# DrawMate G-code Profile
DRAWMATE_GCODE_PROFILE = "drawmate"
DRAWMATE_GCODE_PROFILE_PATH = CONFIG_DIR / "drawmate.toml"

# Canvas Dimensions (US Letter paper with 1-inch margins)
CANVAS_WIDTH_IN_MILLIMETERS = 230
CANVAS_HEIGHT_IN_MILLIMETERS = 170

# AI Configuration
AI_MODEL = "gemini-2.5-flash-image"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VOICE_PROMPT_FILE = LOG_DIR / "stt_log.txt"

# Serial Communication
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
SERIAL_TIMEOUT_IN_SECONDS = 2
