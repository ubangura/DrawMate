import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Global configuration settings"""

    def __init__(self, project_root: Optional[Path] = None):
        # Project root directory
        self.PROJECT_ROOT = (
            Path(project_root).resolve()
            if project_root
            else Path(__file__).resolve().parent.parent.parent
        )

        # Directories
        self.ASSET_DIR = self.PROJECT_ROOT / "assets"
        self.CONFIG_DIR = self.PROJECT_ROOT / "config"
        self.DATA_DIR = self.PROJECT_ROOT / "data"
        self.GCODE_DIR = self.DATA_DIR / "gcode"
        self.LOG_DIR = self.DATA_DIR / "logs"
        self.DATA_ASSET_DIR = self.DATA_DIR / "assets"

        for directory in [self.GCODE_DIR, self.LOG_DIR, self.DATA_ASSET_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

        # Canvas Dimensions
        self.CANVAS_WIDTH_IN_MILLIMETERS = 230.0
        self.CANVAS_HEIGHT_IN_MILLIMETERS = 170.0

        # Serial Communication
        self.SERIAL_PORT = os.getenv("DRAWMATE_SERIAL_PORT", "/dev/ttyACM0")
        self.BAUD_RATE = os.getenv("DRAWMATE_BAUD_RATE", 115200)
        self.SERIAL_TIMEOUT_IN_SECONDS = os.getenv(
            "DRAWMATE_SERIAL_TIMEOUT_IN_SECONDS", 2
        )

        # AI
        self.AI_MODEL = os.getenv("DRAWMATE_AI_MODEL", "gemini-2.5-flash-image")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.DEFAULT_PROMPT = self.CONFIG_DIR / "LineArtContinuationPrompt.md"
        self.VOICE_PROMPT = self.DATA_DIR / "voice_prompt.txt"
        self.VOICE_PROMPT_LOG = self.LOG_DIR / "voice_prompt.log"

        # G-code
        self.GCODE_PROFILE = self.CONFIG_DIR / "drawmate.toml"
        self.GCODE_PROFILE_NAME = "drawmate"


_config: Optional[Config] = None


def get_config(project_root: Optional[Path] = None) -> Config:
    """Get the global configuration object"""
    global _config
    if _config is None:
        _config = Config(project_root)
    return _config
