import numpy as np

def _bresenham(x0, y0, x1, y1):
    """Yields (x, y) pixel coordinates along the line segment."""
    pixels = []
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    x, y = x0, y0

    if dx >= dy:
        err = dx // 2
        while x != x1:
            pixels.append((y, x))        # (row, col) for numpy indexing
            err -= dy
            if err < 0:
                y  += sy
                err += dx
            x += sx
    else:
        err = dy // 2
        while y != y1:
            pixels.append((y, x))
            err -= dx
            if err < 0:
                x  += sx
                err += dy
            y += sy

    pixels.append((y1, x1))
    return pixels

def build_line_cache(nail_positions: list, canvas_size_px: int, diameter_mm: float):
    scale = canvas_size_px / diameter_mm

    # Convert nail mm positions → pixel coordinates
    nail_px = []
    for nail in nail_positions:
        col = int(round(nail['x_mm'] * scale))
        row = int(round(nail['y_mm'] * scale))
        col = max(0, min(canvas_size_px - 1, col))
        row = max(0, min(canvas_size_px - 1, row))
        nail_px.append((row, col))

    n = len(nail_px)
    line_cache = {}

    for i in range(n):
        for j in range(i + 1, n):
            r0, c0 = nail_px[i]
            r1, c1 = nail_px[j]
            pixels = _bresenham(c0, r0, c1, r1)      # bresenham takes x,y; we pass col,row
            # Filter to canvas bounds and convert to numpy index arrays
            valid = [(r, c) for r, c in pixels
                     if 0 <= r < canvas_size_px and 0 <= c < canvas_size_px]
            if valid:
                rows, cols = zip(*valid)
                line_cache[(i, j)] = (np.array(rows), np.array(cols))

    return line_cache, nail_px
