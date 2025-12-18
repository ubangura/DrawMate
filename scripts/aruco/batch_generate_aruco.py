import cv2

# Use DICT_5X5_100 (recommended for your plotter)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)

marker_size = 600  # px
ids_to_generate = [0, 1, 2, 3, 4]

for marker_id in ids_to_generate:
    img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)
    filename = f"markers/aruco_5x5_id{marker_id}.png"
    cv2.imwrite(filename, img)
    print("Saved:", filename)