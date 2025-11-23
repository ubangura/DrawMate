"""DrawMate configuration constants"""
from pathlib import Path

# Directories
ASSET_DIR = Path(__file__).parent / "assets"
GCODE_DIR = Path(__file__).parent / "gcode"

# Canvas Dimensions (A4 paper)
CANVAS_WIDTH_IN_MILLIMETERS = 210
CANVAS_HEIGHT_IN_MILLIMETERS = 297

# Serial Communication
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200
SERIAL_TIMEOUT_IN_SECONDS = 2