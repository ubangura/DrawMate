import cv2
import time

def capture_image(
    device_index=0,
    width=1280,
    height=720,
    output_file="snapshot.jpg"
):
    cap = cv2.VideoCapture(device_index, cv2.CAP_V4L2)

    # Force MJPG (works best in WSL2)
    mjpg = cv2.VideoWriter_fourcc(*"MJPG")
    cap.set(cv2.CAP_PROP_FOURCC, mjpg)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Longer warmup for WSL webcams
    time.sleep(1.0)

    # Debug prints
    print("Width set to:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("Height set to:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("FOURCC actually used:", cap.get(cv2.CAP_PROP_FOURCC))

    ret, frame = cap.read()

    if not ret:
        print("❌ ERROR: Failed to capture frame.")
        cap.release()
        return False

    cv2.imwrite(output_file, frame)
    cap.release()

    print(f"✅ Saved image: {output_file}")
    return True


if __name__ == "__main__":
    capture_image()
