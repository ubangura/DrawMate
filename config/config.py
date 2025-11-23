"""DrawMate configuration constants"""
from pathlib import Path

# Project root directory (DrawMate/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directories
ASSET_DIR = PROJECT_ROOT / "assets"
GCODE_DIR = PROJECT_ROOT / "gcode"

# Canvas Dimensions (A4 paper)
CANVAS_WIDTH_IN_MILLIMETERS = 210
CANVAS_HEIGHT_IN_MILLIMETERS = 297

# Serial Communication
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
SERIAL_TIMEOUT_IN_SECONDS = 2