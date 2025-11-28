from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os

# Output PDF
c = canvas.Canvas("markers/aruco_workspace_test.pdf", pagesize=letter)

# Page size (in points)
PAGE_WIDTH, PAGE_HEIGHT = letter  # 612 x 792 points for letter size

# Marker info
marker_ids = [0, 1, 2, 3]
marker_size = 0.75 * inch     # physical marker size on the printed page
margin = 0.25 * inch          # distance from edges

# Marker placement coordinates for corners
positions = {
    "top_left":     (margin, PAGE_HEIGHT - margin - marker_size),
    "top_right":    (PAGE_WIDTH - margin - marker_size, PAGE_HEIGHT - margin - marker_size),
    "bottom_left":  (margin, margin),
    "bottom_right": (PAGE_WIDTH - margin - marker_size, margin),
}

# Ensure markers directory exists
marker_dir = "markers"

for (corner, (x, y)), marker_id in zip(positions.items(), marker_ids):
    img_path = os.path.join(marker_dir, f"aruco_5x5_id{marker_id}.png")

    c.drawImage(img_path, x, y, width=marker_size, height=marker_size)
    
    # Comment out the line below to ignore id strings
    c.drawString(x, y - 12, f"ID {marker_id} ({corner})")

# Save PDF
c.save()

print("Saved PDF: markers/aruco_workspace_test.pdf")
