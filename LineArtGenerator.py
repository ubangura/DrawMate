from google import genai
from PIL import Image
from pathlib import Path
from typing import Optional
from config.config import AI_MODEL, ASSET_DIR, GEMINI_API_KEY


def _read_file_as_string(file_path: Path) -> str:
    try:
        with open(str(file_path), 'r') as file:
            content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file {file_path} does not exist.")
    return content


class LineArtGenerator:
    def __init__(self, api_key: str = GEMINI_API_KEY):
        self.client = genai.Client(api_key=api_key)

    def generate(self, control_image_path: Path, continuation_prompt_path: Path) -> Optional[Path]:
        """
        Generate line art continuation based on control image and prompt.

        Args:
            control_image_path: Path to the control image
            continuation_prompt_path: Path to the prompt file

        Returns:
            Path to generated image if successful, None if no image was generated

        Raises:
            FileNotFoundError: If the control image or prompt file doesn't exist
            errors.APIError: If API call fails (network, auth, rate limit, etc.)
        """
        try:
            control_image = Image.open(str(control_image_path))
        except FileNotFoundError:
            raise FileNotFoundError(f"Control image {control_image_path} does not exist.")

        response = self.client.models.generate_content(model=AI_MODEL,
                                                       contents=[
                                                           _read_file_as_string(continuation_prompt_path),
                                                           control_image,
                                                       ]
                                                       )

        output_path = ASSET_DIR / (control_image_path.stem + "_continuation.png")
        for part in response.parts:
            if part.inline_data is not None:
                generated_image = part.as_image()
                generated_image.save(str(output_path))
                return output_path

        return None
