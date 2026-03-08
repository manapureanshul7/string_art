import numpy as np
from PIL import Image, ImageDraw

def render_string_art(nail_sequence: list, nail_px: list,
                      canvas_size_px: int, config: dict,
                      output_path: str = "./output/preview.png"):

    # White background
    img  = Image.new('RGB', (canvas_size_px, canvas_size_px), (255, 255, 255))
    draw = ImageDraw.Draw(img, 'RGBA')

    thread      = config['threads'][0]
    color_hex   = thread['color_hex']
    r           = int(color_hex[1:3], 16)
    g           = int(color_hex[3:5], 16)
    b           = int(color_hex[5:7], 16)
    line_color  = (r, g, b, 25)   # very transparent — layering builds darkness naturally

    # Draw each segment
    for i in range(len(nail_sequence) - 1):
        n0         = nail_sequence[i]
        n1         = nail_sequence[i + 1]
        row0, col0 = nail_px[n0]
        row1, col1 = nail_px[n1]
        draw.line([(col0, row0), (col1, row1)], fill=line_color, width=1)

    # Draw nails as small dots
    nail_color = (180, 0, 0)
    for row, col in nail_px:
        draw.ellipse([(col-2, row-2), (col+2, row+2)], fill=nail_color)

    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"  Preview saved → {output_path}")
    return img
