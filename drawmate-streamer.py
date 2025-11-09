"""
DrawMate G-code Streamer
-------------------------
Streams a G-code file to a GRBL-controlled Arduino (CNC shield).

Usage:
    python drawmate_streamer.py /dev/ttyACM0 gcode/cat.gcode

Author: DrawMate Project
"""

import serial
import time
import sys
from pathlib import Path


def send_gcode_file(port: str, gcode_path: Path, baudrate: int = 115200, timeout: int = 1):
    """
    Send a G-code file line by line to a GRBL device over serial.

    Args:
        port: Serial port (e.g., '/dev/ttyACM0' or 'COM3')
        gcode_path: Path to G-code file
        baudrate: Baud rate for GRBL (default: 115200)
        timeout: Serial timeout in seconds
    """

    if not gcode_path.exists():
        print(f"[!] G-code file not found: {gcode_path}")
        return

    print(f"📡 Connecting to GRBL on {port} at {baudrate} baud...")
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as grbl:
            # Wake up GRBL
            grbl.write(b"\r\n\r\n")
            time.sleep(2)
            grbl.flushInput()
            print("✅ GRBL connected. Beginning stream...\n")

            with open(gcode_path, "r") as gcode_file:
                for line in gcode_file:
                    command = line.strip()
                    if not command or command.startswith(";"):  # skip blanks/comments
                        continue

                    # Send the line
                    grbl.write((command + "\n").encode())
                    print(f"→ {command}")

                    # Wait for response
                    response = grbl.readline().decode().strip()
                    while not response:
                        response = grbl.readline().decode().strip()
                    print(f"   ← {response}")

                    # Optional short delay to avoid buffer overflow
                    time.sleep(0.05)

            # Soft reset at the end (optional)
            grbl.write(b"\x18")
            print("\n✅ G-code stream complete.")
            print("🔄 GRBL reset sent. Plotter returning to idle.\n")

    except serial.SerialException as e:
        print(f"[!] Serial connection error: {e}")
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user. Stopping stream.")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python drawmate_streamer.py <serial_port> <gcode_path>")
        print("Example: python drawmate_streamer.py /dev/ttyUSB0 gcode/cat.gcode")
        sys.exit(1)

    port = sys.argv[1]
    gcode_path = Path(sys.argv[2])
    send_gcode_file(port, gcode_path)
