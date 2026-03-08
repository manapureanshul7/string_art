import numpy as np

def run_greedy(target_img: np.ndarray, nail_count: int,
               line_cache: dict, config: dict) -> list:

    algo           = config['algorithm']
    max_lines      = algo['max_lines']
    skip_neighbors = algo['skip_neighbors']
    opacity        = algo.get('opacity', 0.2)   # replaces line_darkness

    # Rendered canvas starts white (1.0)
    canvas = np.ones_like(target_img)

    current_nail  = 0
    nail_sequence = [current_nail]

    for step in range(max_lines):
        best_nail  = None
        best_score = -1.0

        for candidate in range(nail_count):
            if candidate == current_nail:
                continue

            dist = abs(candidate - current_nail)
            dist = min(dist, nail_count - dist)
            if dist < skip_neighbors:
                continue

            key = (min(current_nail, candidate), max(current_nail, candidate))
            if key not in line_cache:
                continue

            rows, cols  = line_cache[key]
            pixel_count = len(rows)
            if pixel_count < 20:
                continue

            # Score = improvement: how much target darkness is uncovered here
            current_darkness  = 1.0 - canvas[rows, cols]       # how dark canvas is now
            target_darkness   = target_img[rows, cols]          # how dark it should be
            improvement       = target_darkness - current_darkness
            score = float(np.sum(np.maximum(improvement, 0))) / (pixel_count ** 0.5)

            if score > best_score:
                best_score = score
                best_nail  = candidate

        # Natural stop: no line makes things better
        if best_nail is None or best_score <= 0:
            print(f"  Natural stop at step {step + 1}")
            break

        # Draw line: darken canvas pixels (capped at black)
        rows, cols = line_cache[(min(current_nail, best_nail),
                                  max(current_nail, best_nail))]
        canvas[rows, cols] *= (1.0 - opacity)

        nail_sequence.append(best_nail)
        current_nail = best_nail

        if (step + 1) % 500 == 0:
            print(f"  Step {step + 1}/{max_lines}  score={best_score:.5f}")

    return nail_sequence
