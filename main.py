from config.config import ASSET_DIR, BAUD_RATE, CANVAS_WIDTH_IN_MILLIMETERS, CANVAS_HEIGHT_IN_MILLIMETERS, GCODE_DIR, SERIAL_PORT, SERIAL_TIMEOUT_IN_SECONDS
from GCodeConverter import GCodeConverter
from DrawMateStreamer import DrawMateStreamer
from pathlib import Path
import sys


def main():
    # Check for command-line argument
    if len(sys.argv) > 1:
        INPUT_IMAGE = Path(sys.argv[1])
        if not INPUT_IMAGE.exists():
            print(f"[!] Image file not found: {INPUT_IMAGE}")
            return
        print(f"🖼️ Using input image: {INPUT_IMAGE}")
    else:
        INPUT_IMAGE = ASSET_DIR / "bird.jpg"
        print(f"🖼️ No image argument provided. Using default: {INPUT_IMAGE}")

    # === Conversion pipeline ===
    gcode_converter = GCodeConverter(
        ASSET_DIR,
        GCODE_DIR,
        CANVAS_WIDTH_IN_MILLIMETERS,
        CANVAS_HEIGHT_IN_MILLIMETERS
    )

    print("🖼️  Step 1: Converting raster to SVG...")
    svg_file_path = gcode_converter.raster_to_svg(INPUT_IMAGE)

    print("⚙️  Step 2: Converting SVG to G-code...")
    gcode_path = gcode_converter.svg_to_gcode(svg_file_path)

    print(f"✅ G-code file created: {gcode_path}")

    # === Stream to DrawMate ===
    print("📡 Step 3: Streaming G-code to DrawMate...")
    streamer = DrawMateStreamer(SERIAL_PORT, BAUD_RATE, SERIAL_TIMEOUT_IN_SECONDS)
    streamer.stream_gcode(gcode_path)

    print("🎉 Done! The DrawMate should now be plotting.")


if __name__ == "__main__":
    main()
