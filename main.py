import yaml
from src.canvas      import compute_nail_positions
from src.image_utils import load_and_preprocess
from src.line_cache  import build_line_cache
from src.algorithm   import run_greedy
from src.exporter    import export_instructions
from src.visualizer  import render_string_art 

def main():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    canvas         = config['canvas']
    canvas_size_px = canvas.get('canvas_resolution_px', int(canvas['diameter_mm']))

    print("=== String Art Builder — B&W Mode ===\n")

    print("[1/4] Computing nail positions...")
    nail_positions = compute_nail_positions(config)
    print(f"      {len(nail_positions)} nails on a {canvas['diameter_mm']}mm circle\n")

    print("[2/4] Loading and preprocessing image...")
    error_img = load_and_preprocess(config['input_image'], canvas_size_px)
    print(f"      Canvas: {canvas_size_px}x{canvas_size_px} px\n")

    print("[3/4] Building line cache...")
    line_cache, nail_px = build_line_cache(
        nail_positions, canvas_size_px, canvas['diameter_mm']
    )
    print(f"      {len(line_cache)} segments cached\n")

    print("[4/4] Running greedy algorithm...")
    nail_sequence = run_greedy(error_img, len(nail_positions), line_cache, config)
    print(f"      {len(nail_sequence) - 1} lines generated\n")

    print("Exporting instructions...")
    export_instructions(nail_sequence, nail_positions, config)
    render_string_art(                                  # ← new
        nail_sequence, nail_px,
        canvas_size_px, config,
        output_path="./output/preview.png"
    )
    print("\n✓ Done.")

if __name__ == '__main__':
    main()
