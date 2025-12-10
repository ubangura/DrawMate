#!/usr/bin/env python3
import sounddevice as sd
import queue
import sys
import json
import os
from datetime import datetime
from vosk import Model, KaldiRecognizer

# ----------------------
# Global configuration
# ----------------------

# 1) Path to the English Vosk model
MODEL_PATH = "/home/matthewandjun/stt_models/vosk-model-small-en-us-0.15"

# 2) Logging directory & files
LOG_DIR = "/home/matthewandjun/Desktop/DrawMate/config"
LOG_FILE = os.path.join(LOG_DIR, "stt_log.txt")
LATEST_FILE = os.path.join(LOG_DIR, "latest_prompt.txt")

# 3) Audio configuration
SAMPLE_RATE = 16000
CHANNELS = 1

# 4) Audio queue
q: "queue.Queue[bytes]" = queue.Queue()


# --------------------------------------------------
# Audio callback
# --------------------------------------------------
def audio_callback(indata, frames, time, status):
    """Called from the audio thread; push raw bytes into the queue."""
    if status:
        print(status, file=sys.stderr)

    # If you want to debug volume, uncomment:
    # import numpy as np
    # vol = int(np.abs(indata).mean() * 10000)
    # print("volume:", vol)

    q.put(bytes(indata))


def select_input_device() -> int | None:
    """
    Pick the first device that has at least 1 input channel.
    Returns the device index, or None if none is found.
    """
    devices = sd.query_devices()
    print("🔊 Available audio devices:")
    for i, dev in enumerate(devices):
        print(f"  {i}: {dev['name']} (in={dev['max_input_channels']}, out={dev['max_output_channels']})")

    for i, dev in enumerate(devices):
        if dev["max_input_channels"] > 0:
            print(f"🎤 Using input device {i}: {dev['name']}")
            return i

    print("❌ No device with input channels found.")
    return None


# --------------------------------------------------
# Main STT logic
# --------------------------------------------------
def main() -> None:
    # Check model exists
    if not os.path.exists(MODEL_PATH):
        print("Model folder not found:", MODEL_PATH)
        return

    # Ensure log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    print("🎙 Loading Vosk English model... (may take a few seconds)")
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)

    # Pick a microphone device
    mic_device = select_input_device()
    if mic_device is None:
        return

    print("✅ Ready! Speak English into the microphone. (Ctrl+C to exit)")

    # Open audio stream – InputStream is friendlier than RawInputStream
    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=8000,
            dtype="int16",
            channels=CHANNELS,
            callback=audio_callback,
            device=mic_device,
        ):
            try:
                while True:
                    data = q.get()

                    if recognizer.AcceptWaveform(data):
                        result_json = recognizer.Result()
                        result = json.loads(result_json)
                        text = result.get("text", "").strip()

                        if text:
                            print("▶ recognized:", text)

                            # ----------------------------------------
                            # Save to full log
                            # ----------------------------------------
                            try:
                                with open(LOG_FILE, "a", encoding="utf-8") as f:
                                    f.write(f"{datetime.now().isoformat()}  {text}\n")
                            except Exception as e:
                                print(f"Cannot write log file: {e}", file=sys.stderr)

                            # ----------------------------------------
                            # Save latest recognized line
                            # ----------------------------------------
                            try:
                                with open(LATEST_FILE, "w", encoding="utf-8") as f:
                                    f.write(text + "\n")
                            except Exception as e:
                                print(f"Cannot write latest prompt file: {e}", file=sys.stderr)
                    else:
                        # You can inspect partial results if you’d like:
                        # partial = json.loads(recognizer.PartialResult()).get("partial", "")
                        # if partial:
                        #     print("… partial:", partial)
                        pass

            except KeyboardInterrupt:
                print("\n🛑 Exiting.")
                final_json = recognizer.FinalResult()
                final = json.loads(final_json).get("text", "")
                if final:
                    print("Final:", final)

    except sd.PortAudioError as e:
        print(f"❌ PortAudio error while opening input stream: {e}", file=sys.stderr)
        print("Hint: check the selected device index and that your mic isn't muted or in use.", file=sys.stderr)


if __name__ == "__main__":
    main()
