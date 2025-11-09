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
        """Establish and initialize the serial connection to GRBL."""
        print(f"📡 Connecting to GRBL on {self.port} at {self.baudrate} baud...")
        grbl = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        grbl.write(b"\r\n\r\n")  # wake up GRBL
        time.sleep(2)

        # Read any startup text (like "Grbl 1.1h")
        startup_msg = grbl.read_all().decode(errors="ignore").strip()
        if startup_msg:
            print(f"💬 Startup message:\n{startup_msg}\n")

        # Unlock if alarmed
        print("🔓 Sending unlock command ($X)...")
        grbl.write(b"$X\n")
        time.sleep(0.5)
        grbl.flushInput()

        print("✅ GRBL ready to receive commands.\n")
        return grbl

    def _send_line(self, grbl, line: str):
        """Send a single line of G-code and wait for a response."""
        grbl.write((line + "\n").encode())
        print(f"→ {line}")

        response = grbl.readline().decode().strip()
        while not response:
            response = grbl.readline().decode().strip()
        print(f"   ← {response}")

    # -------------------------------
    # Public Method
    # -------------------------------
    def stream_gcode(self, gcode_path: Path):
        """Stream a G-code file to GRBL."""
        gcode_path = Path(gcode_path)
        if not gcode_path.exists():
            print(f"[!] G-code file not found: {gcode_path}")
            return

        try:
            with self._connect() as grbl, open(gcode_path, "r") as gfile:
                print("🚀 Beginning G-code stream...\n")

                for raw_line in gfile:
                    line = raw_line.strip()
                    if not line or line.startswith(";"):  # skip comments
                        continue

                    self._send_line(grbl, line)
                    time.sleep(0.05)  # avoid GRBL buffer overflow

                # Optional: soft reset GRBL after completion
                grbl.write(b"\x18")
                print("\n✅ Stream complete. GRBL reset and returning to idle.\n")

        except serial.SerialException as e:
            print(f"[!] Serial connection error: {e}")
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user. Stopping stream.")
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
