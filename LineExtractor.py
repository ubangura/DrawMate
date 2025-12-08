import cv2
import numpy as np
from skimage.morphology import skeletonize

ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)

class LineExtractor:
    def __init__(self,
                 workspace_width_px=2200,
                 workspace_height_px=1700,
                 marker_ids=(0, 1, 2, 3)):
        """
        marker_ids: (TL, TR, BL, BR)
        """
        self.W = workspace_width_px
        self.H = workspace_height_px
        self.marker_ids = marker_ids

    # ----------------------------------------------------------------------
    # MARKER DETECTION + HOMOGRAPHY
    # ----------------------------------------------------------------------
    def _sort_markers(self, corners, ids):
        found = {}
        for corner, mid in zip(corners, ids.flatten()):
            c = corner[0]
            cx = np.mean(c[:, 0])
            cy = np.mean(c[:, 1])
            found[mid] = (cx, cy)

        TL, TR, BL, BR = self.marker_ids
        missing = [m for m in (TL, TR, BL, BR) if m not in found]
        if missing:
            raise ValueError(f"Missing markers: {missing}")

        return {
            "TL": found[TL],
            "TR": found[TR],
            "BL": found[BL],
            "BR": found[BR]
        }

    def _compute_homography(self, frame):
        corners, ids, _ = cv2.aruco.detectMarkers(frame, ARUCO_DICT)
        if ids is None or len(ids) < 4:
            raise ValueError("Not all 4 ArUco markers detected.")

        sorted_pts = self._sort_markers(corners, ids)

        src = np.float32([
            sorted_pts["TL"],
            sorted_pts["TR"],
            sorted_pts["BL"],
            sorted_pts["BR"]
        ])

        dst = np.float32([
            [0, 0],
            [self.W, 0],
            [0, self.H],
            [self.W, self.H]
        ])

        H, _ = cv2.findHomography(src, dst)
        return H

    # ----------------------------------------------------------------------
    # LINE EXTRACTION
    # ----------------------------------------------------------------------
    def _extract_line_mask(self, warped):
        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 1)
        edges = cv2.Canny(blur, 40, 120)

        kernel = np.ones((3, 3), np.uint8)
        dil = cv2.dilate(edges, kernel, iterations=1)
        er = cv2.erode(dil, kernel, iterations=1)

        # Convert to skeleton for thin vectorizable lines
        skel = skeletonize(er > 0).astype(np.uint8) * 255
        return skel

    # ----------------------------------------------------------------------
    # VECTORIZE: Convert skeleton pixels → polylines
    # ----------------------------------------------------------------------
    def _trace_paths(self, mask):
        h, w = mask.shape
        visited = np.zeros_like(mask, dtype=bool)
        paths = []

        # Offsets for 8-connected neighbors
        nbrs = [(-1,-1), (-1,0), (-1,1),
                 (0,-1),         (0,1),
                 (1,-1),  (1,0), (1,1)]

        def neighbors(x, y):
            out = []
            for dx, dy in nbrs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    if mask[ny, nx] > 0:
                        out.append((nx, ny))
            return out

        for y in range(h):
            for x in range(w):
                if mask[y, x] == 0 or visited[y, x]:
                    continue

                # Start a new stroke
                stack = [(x, y)]
                stroke = []

                while stack:
                    px, py = stack.pop()
                    if visited[py, px]:
                        continue

                    visited[py, px] = True
                    stroke.append((px, py))

                    for nx, ny in neighbors(px, py):
                        if not visited[ny, nx]:
                            stack.append((nx, ny))

                if len(stroke) > 3:
                    paths.append(stroke)

        return paths

    # ----------------------------------------------------------------------
    # PUBLIC API CALL
    # ----------------------------------------------------------------------
    def extract(self, image_path):
        """
        Returns:
            warped_image   (top-down corrected view)
            paths_px       (list of stroke paths in pixel coords)
            paths_mm       (list of stroke paths converted to mm)
        """
        frame = cv2.imread(image_path)
        if frame is None:
            raise FileNotFoundError(image_path)

        H = self._compute_homography(frame)
        warped = cv2.warpPerspective(frame, H, (self.W, self.H))

        mask = self._extract_line_mask(warped)
        paths_px = self._trace_paths(mask)

        # Convert pixels → mm (scale to your real workspace size)
        MM_PER_PX_X = 220 / self.W
        MM_PER_PX_Y = 170 / self.H

        paths_mm = [
            [(x * MM_PER_PX_X, y * MM_PER_PX_Y) for (x, y) in stroke]
            for stroke in paths_px
        ]

        return warped, paths_px, paths_mm
