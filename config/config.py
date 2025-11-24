"""DrawMate configuration constants"""
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Directories

# Project root directory (DrawMate/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

ASSET_DIR = PROJECT_ROOT / "assets"
GCODE_DIR = PROJECT_ROOT / "gcode"
CONFIG_DIR = PROJECT_ROOT / "config"

# Canvas Dimensions (US Letter paper with 1-inch margins)
CANVAS_WIDTH_IN_MILLIMETERS = 190
CANVAS_HEIGHT_IN_MILLIMETERS = 254

# AI Configuration
AI_MODEL = "gemini-2.5-flash-image"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Serial Communication
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
SERIAL_TIMEOUT_IN_SECONDS = 2