# String Art Builder — Project Context Document
**Last Updated:** 2026-03-08
**Current Phase:** Phase 1 — Algorithm Development (B&W baseline working)
**One-liner:** A two-part system that converts an image into physical string art
               using a software algorithm and a robotics-driven execution machine.

---

## Architecture Overview

**Part 1 — Software Pipeline**
Takes an image as input and outputs an ordered sequence of nail indices (and
optionally thread color assignments) that approximate the image in string art
form. Output is a machine-readable instruction file (JSON) fed to the
microcontroller.

**Part 2 — Hardware Execution**
A microcontroller (likely Arduino Mega + RAMPS 1.4) drives actuators that
physically wrap thread around nails on a board, following the instruction file
from Part 1. Design is still being explored.

**Overall Data Flow:**
Image → Preprocessing → Algorithm → Nail Sequence + Color Assignments
→ instructions.json → Microcontroller → Actuators → Physical String Art

---

## Project File Structure
string_art_builder/
├── config.yaml
├── main.py
├── src/
│   ├── __init__.py
│   ├── canvas.py          # nail position computation
│   ├── image_utils.py     # image loading & preprocessing
│   ├── line_cache.py      # precompute all nail-pair pixel maps (Bresenham)
│   ├── algorithm.py       # greedy algorithm (multiplicative decay model)
│   ├── visualizer.py      # renders preview.png from nail sequence
│   └── exporter.py        # writes instructions.json
├── input/                 # place input images here
└── output/
    ├── instructions.json
    └── preview.png

---

## Key Design Decisions

### Agreed / Baseline
- **Algorithm:** Greedy with length-normalized sum scoring
  `score = sum(improvement) / sqrt(pixel_count)`
- **Darkening model:** Multiplicative decay `canvas *= (1 - opacity)`
  NOT additive — additive causes concentric ring artifacts
- **Scoring model:** Improvement-based — score = target darkness minus
  current canvas darkness, clamped to positive only
- **Natural stop:** Algorithm halts when best_score <= 0 (no line improves
  canvas); max_lines is a safety ceiling only
- **Diminishing returns:** Beyond ~3000–5000 lines on a 500mm/250-nail board,
  additional lines are largely redundant physically and visually
- **Preprocessing:**
  - Center-crop to square → resize → autocontrast (cutoff=2) → invert
  - Gamma correction (0.7) to boost mid-tones (eyebrows, fine features)
  - Circular mask applied to zero out corners outside the board
  - Edge blending: REMOVED — made results worse, introduced harsh clusters
- **Nail count:** ~261 nails at 6mm spacing on 500mm diameter board
  (formula: floor(π * diameter / spacing))
- **Circular board** is primary target; rectangular is future scope
- **Rotating-board approach** for hardware (lazy Susan — nail comes to
  wrapping station)
- **Glue-dot tie-off** instead of robotic knot-tying (for V1)
- **B&W string art** is current baseline; color is planned extension

### User-Configurable Parameters (can change anytime, via config.yaml)
- Canvas size (diameter_mm) and shape
- Nail spacing (determines nail count automatically)
- Canvas resolution in pixels (canvas_resolution_px)
- Per-thread: color_hex, material, thickness_mm, opacity, max_tension_N,
  z_priority, available
- max_lines, skip_neighbors, gamma, lines_per_round

### Color Mode Design (planned, not yet implemented)
- k-means clustering on image → match to available thread colors (LAB space)
- Per-channel greedy passes with interleaved rounds for same z_priority threads
- Different z_priority groups execute fully before next group begins
- Instruction file has multiple sequence objects, one per thread segment
- Microcontroller executes flat sequence top-to-bottom; ordering logic
  lives entirely in software

### Explicitly Ruled Out (for V1)
- Cartesian/SCARA arm for hardware
- Robotic knot-tying
- Edge blending in preprocessing

### Still Open / Undecided
- Final microcontroller choice (Arduino Mega + RAMPS 1.4 likely)
- Number and types of actuators (thread feed, wrap arm, cutter)
- Board orientation (vertical preferred, not finalized)
- Camera feedback for wrap verification
- Frontend tech stack (FastAPI + React + Vite planned)
- Importance map / face-detection based weighting (future quality improvement)

---

## Current config.yaml (working baseline)

```yaml
canvas:
  shape: circular
  diameter_mm: 500
  nail_spacing_mm: 6         # ~261 nails
  nail_diameter_mm: 2
  canvas_resolution_px: 700

input_image: input/image.jpg

algorithm:
  mode: bw
  max_lines: 6000            # safety ceiling; natural stop usually earlier
  skip_neighbors: 20
  gamma: 0.7                 # boosts mid-tones; 1.0 = no change
  lines_per_round: 200

threads:
  - id: T1
    color_hex: "#1a1a1a"
    material: cotton
    thickness_mm: 0.5
    opacity: 0.3             # per-thread; models physical thread opacity
    max_tension_N: 15.0
    z_priority: 1
    available: true

output:
  format: json
  filepath: ./output/instructions.json
  include_nail_positions: true
