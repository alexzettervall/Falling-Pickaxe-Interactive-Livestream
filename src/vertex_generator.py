import numpy as np
import cv2

# Load image with alpha channel
img = cv2.imread(
    '../texture-packs/Default-Java-1.21.5/assets/minecraft/textures/item/wooden_pickaxe.png',
    cv2.IMREAD_UNCHANGED
)

if img.shape[2] != 4:
    raise ValueError("Image has no alpha channel")

height, width = img.shape[:2]
alpha = img[:, :, 3]

# Create binary mask of non-transparent pixels
mask = np.where(alpha > 0, 255, 0).astype(np.uint8)

# Use Canny edge detection to get pixel-perfect edges
edges = cv2.Canny(mask, 50, 150)

# Find contours of edges, in order
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Loop through contour points, normalize, and print
for contour in contours:
    for point in contour:
        x, y = point[0]
        x_norm = (x / width) - 0.5
        y_norm = (y / height) - 0.5
        print(f"({x_norm}, {y_norm}), ")
