from config import CANVAS_WIDTH_IN_MILLIMETERS, CANVAS_HEIGHT_IN_MILLIMETERS
from GCodeConverter import GCodeConverter
from pathlib import Path


def main():
    gcode_converter = GCodeConverter(Path(__file__).parent / "assets",
                                     CANVAS_WIDTH_IN_MILLIMETERS,
                                     CANVAS_HEIGHT_IN_MILLIMETERS
                                     )
    svg_file_path = gcode_converter.raster_to_svg(Path("assets/bird.jpg"))
    gcode_converter.svg_to_gcode(svg_file_path)


if __name__ == "__main__":
    main()
