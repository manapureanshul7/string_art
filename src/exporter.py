import json
import os
from datetime import datetime

def export_instructions(nail_sequence: list, nail_positions: list, config: dict):
    thread   = config['threads'][0]       # B&W mode: single thread
    out_cfg  = config['output']
    canvas   = config['canvas']

    instructions = {
        "metadata": {
            "generated_at":      datetime.now().isoformat(),
            "canvas_shape":      canvas['shape'],
            "canvas_diameter_mm": canvas.get('diameter_mm'),
            "nail_count":        len(nail_positions),
            "total_lines":       len(nail_sequence) - 1,
            "mode":              config['algorithm']['mode']
        },
        "nail_positions": nail_positions if out_cfg.get('include_nail_positions') else [],
        "sequences": [
            {
                "thread_id":  thread['id'],
                "color_hex":  thread['color_hex'],
                "nails":      nail_sequence
            }
        ]
    }

    filepath = out_cfg['filepath']
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(instructions, f, indent=2)

    print(f"  Saved → {filepath}")
    return instructions
