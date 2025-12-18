import cv2
import argparse
import os

# -------------------------
# Parse command line args
# -------------------------
parser = argparse.ArgumentParser(description="Generate an ArUco marker image.")
parser.add_argument(
    "marker_id",
    type=int,
    help="ID of the ArUco marker to generate (e.g. 0, 1, 2, 3)"
)
parser.add_argument(
    "--size",
    type=int,
    default=600,
    help="Marker size in pixels (default: 600)"
)
parser.add_argument(
    "--out",
    type=str,
    default="markers",
    help="Output directory (default: markers)"
)

args = parser.parse_args()

marker_id = args.marker_id
marker_size = args.size
output_dir = args.out

# -------------------------
# Prepare dictionary
# -------------------------
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)

# -------------------------
# Generate the marker
# -------------------------
marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

# -------------------------
# Save output
# -------------------------
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"aruco_5x5_id{marker_id}.png")

cv2.imwrite(output_path, marker_img)

print("Saved:", output_path)
