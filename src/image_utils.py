from math import gamma

import numpy as np
from PIL import Image, ImageOps
import cv2

def load_and_preprocess(image_path: str, canvas_size_px: int) -> np.ndarray:
    img = Image.open(image_path).convert('L')

    # Step 1: Center-crop to square (preserves aspect ratio)
    w, h   = img.size
    side   = min(w, h)
    left   = (w - side) // 2
    top    = (h - side) // 2
    img    = img.crop((left, top, left + side, top + side))

    # Step 2: Resize to canvas resolution
    img = img.resize((canvas_size_px, canvas_size_px), Image.LANCZOS)
    img = ImageOps.autocontrast(img, cutoff=2) # boost contrast for better string art results
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = 1.0 - arr     # invert: dark pixels = high error = high priority
    gamma = 0.7    # < 1.0 boosts mid-tones; add to config later
    arr   = np.power(arr, gamma)

    # Step 3: Apply circular mask — zero out corners outside the board
    cy, cx = canvas_size_px / 2, canvas_size_px / 2
    radius = canvas_size_px / 2
    Y, X   = np.ogrid[:canvas_size_px, :canvas_size_px]
    mask   = (X - cx)**2 + (Y - cy)**2 <= radius**2
    arr[~mask] = 0.0    # outside circle contributes nothing to scoring

    return arr
