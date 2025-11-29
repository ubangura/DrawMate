"""
DrawMate: Image to GRBL G-code Pipeline

Converts raster images to optimized G-code for pen plotters using GRBL.
Uses ImageMagick for preprocessing, Potrace for vectorization, and vpype for optimization.
"""
import subprocess
from pathlib import Path


class GCodeConverter:
    """
    Converts raster images to GRBL-compatible G-code for pen plotters.

    The conversion pipeline:
    1. Raster image → Bitmap (ImageMagick)
    2. Bitmap → SVG (Potrace)
    3. SVG → Optimized SVG (vpype)
    4. SVG → G-code (vpype-gcode)
    """

    def __init__(self,
                 asset_directory: Path,
                 gcode_directory: Path,
                 canvas_width_in_millimeters: float,
                 canvas_height_in_millimeters: float
                 ):
        self.canvas_width_in_millimeters = canvas_width_in_millimeters
        self.canvas_height_in_millimeters = canvas_height_in_millimeters

        self.asset_directory = asset_directory
        self.gcode_directory = gcode_directory
        self.gcode_directory.mkdir(exist_ok=True)

    def raster_to_svg(self, input_image_path: Path) -> Path:
        """
        Convert raster image to optimized SVG.

        Args:
            input_image_path: Path to input raster image (PNG, JPG, etc.)

        Returns:
            Path to an optimized SVG file

        Raises:
            FileNotFoundError: If the input image doesn't exist
            subprocess.CalledProcessError: If conversion fails
        """
        if not input_image_path.exists():
            raise FileNotFoundError(f"Image file {input_image_path} does not exist.")

        output_svg_path = self.asset_directory / f"{input_image_path.stem}.svg"

        # Convert to bitmap and trace to SVG
        try:
            bitmap_process = subprocess.Popen(
                ["convert", str(input_image_path), "-threshold", "50%", "bmp:-"],
                stdout=subprocess.PIPE
            )

            subprocess.run(
                ["potrace", "-s", "-o", str(output_svg_path), "-"],
                stdin=bitmap_process.stdout,
                check=True,
                capture_output=True
            )
            bitmap_process.wait(timeout=30)

        except subprocess.TimeoutExpired:
            bitmap_process.kill()
            raise
        except subprocess.CalledProcessError:
            raise

        # Optimize with Vpype
        try:
            subprocess.run([
                "vpype",
                "read", str(output_svg_path),
                "linesimplify", "--tolerance", "0.2mm",
                "linemerge",
                "linesort",
                "layout", "-m 3mm", "--landscape", f"{self.canvas_width_in_millimeters}x{self.canvas_height_in_millimeters}mm",
                "write", str(output_svg_path),
            ], check=True, capture_output=True, text=True
            )

            print(f"SVG optimized: {output_svg_path}")
            return output_svg_path

        except subprocess.CalledProcessError:
            raise

    def svg_to_gcode(self, input_svg_path: Path) -> Path:
        """
        Convert SVG to GRBL-compatible G-code.

        Args:
            input_svg_path: Path to an input SVG file

        Returns:
            Path to a generated G-code file

        Raises:
            FileNotFoundError: If the input SVG doesn't exist
            subprocess.CalledProcessError: If G-code generation fails
        """
        if not input_svg_path.exists():
            raise FileNotFoundError(f"SVG file {input_svg_path} does not exist.")

        output_gcode_path = self.gcode_directory / f"{input_svg_path.stem}.gcode"

        try:
            subprocess.run([
                "vpype",
                "--config", str(Path("./config/drawmate.toml")),
                "read", str(input_svg_path),
                "gwrite",
                "--profile", "drawmate",
                str(output_gcode_path),
            ], check=True, capture_output=True, text=True
            )

            print(f"G-code created: {output_gcode_path}")
            return output_gcode_path

        except subprocess.CalledProcessError:
            raise
