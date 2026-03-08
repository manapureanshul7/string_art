import math

def compute_nail_positions(config):
    canvas = config['canvas']
    shape = canvas['shape']

    if shape == 'circular':
        diameter_mm = canvas['diameter_mm']
        radius_mm   = diameter_mm / 2
        spacing_mm  = canvas['nail_spacing_mm']

        nail_count = int(math.pi * diameter_mm / spacing_mm)
        cx, cy     = diameter_mm / 2, diameter_mm / 2

        nails = []
        for i in range(nail_count):
            angle = 2 * math.pi * i / nail_count
            x = cx + radius_mm * math.cos(angle)
            y = cy + radius_mm * math.sin(angle)
            nails.append({'id': i, 'x_mm': round(x, 3), 'y_mm': round(y, 3)})

        return nails

    else:
        raise NotImplementedError("Rectangular canvas is planned but not yet supported.")
