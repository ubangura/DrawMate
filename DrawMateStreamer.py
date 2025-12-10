"""
DrawMate G-code Streamer
-------------------------
Streams a G-code file to a GRBL-controlled Arduino (CNC shield).

Usage (standalone):
    python DrawMateStreamer.py /dev/ttyACM0 gcode/cat.gcode

Usage (imported):
    from DrawMateStreamer import DrawMateStreamer
    streamer = DrawMateStreamer("/dev/ttyACM0")
    streamer.stream_gcode("gcode/cat.gcode")

Author: DrawMate Project
"""

import serial
import time
import sys
from pathlib import Path


class DrawMateStreamer:
    """Handles serial communication and G-code streaming to GRBL."""

    def __init__(self, port: str, baudrate: int = 115200, timeout: int = 1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    # -------------------------------
    # Internal Helpers
    # -------------------------------
    def _connect(self):
        """Establish and initialize serial connection to GRBL."""
        print(f"📡 Connecting to GRBL on {self.port} at {self.baudrate} baud...")

        grbl = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        time.sleep(1)

        # --- Soft reset (CTRL-X) ---
        print("🔄 Sending soft reset (CTRL-X)...")
        grbl.write(b"\x18")
        time.sleep(2)

        # Read startup message
        startup = grbl.read_all().decode(errors="ignore").strip()
        if startup:
            print(f"💬 Startup message:\n{startup}\n")

        # --- Unlock GRBL if alarmed ---
        print("🔓 Unlocking GRBL ($X)...")
        grbl.write(b"$X\n")
        time.sleep(0.5)
        grbl.flushInput()

        print("✅ GRBL ready.\n")
        return grbl


    def _send_line(self, grbl, line: str):
        grbl.write((line + "\n").encode())
        print(f"→ {line}")

        # Read response safely
        for _ in range(40):  # ~4 seconds
            response = grbl.readline().decode().strip()
            if response:
                print(f"   ← {response}")
                return

        print("   ⚠️ No response received (timeout).")


    # -------------------------------
    # Public Method
    # -------------------------------
    def stream_gcode(self, gcode_path: Path):
        gcode_path = Path(gcode_path)

        if not gcode_path.exists():
            print(f"[!] G-code file not found: {gcode_path}")
            return

        try:
            grbl = self._connect()
            print("🚀 Beginning G-code stream...\n")

            with open(gcode_path, "r") as gfile:
                for raw_line in gfile:
                    line = raw_line.strip()
                    if not line or line.startswith(";"):
                        continue

                    self._send_line(grbl, line)
                    time.sleep(0.05)

            print("\n✅ G-code stream finished.")
            grbl.close()

        except serial.SerialException as e:
            print(f"[!] Serial connection error: {e}")
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user.")
        except Exception as e:
            print(f"[!] Unexpected error: {e}")



# -------------------------------
# Standalone CLI Interface
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python DrawMateStreamer.py <serial_port> <gcode_path>")
        print("Example: python DrawMateStreamer.py /dev/ttyACM0 gcode/cat.gcode")
        sys.exit(1)

    port = sys.argv[1]
    gcode_path = Path(sys.argv[2])

    streamer = DrawMateStreamer(port)
    streamer.stream_gcode(gcode_path)
