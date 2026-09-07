# avogadro-xyzrender

Publication-quality molecular graphics from Avogadro 2 using
[xyzrender](https://github.com/aligfellow/xyzrender).

Adds two items to **File → Export**:

- **Rendered Image (xyzrender)...** — a still SVG, PNG, PDF, or TIFF
- **Rendered Animation (xyzrender)...** — a rotating animated GIF

The current molecule is passed to xyzrender as CJSON, Avogadro's native
format, so bond orders, per-atom colors, unit cells, and the saved camera
orientation all carry over. It is rendered with the chosen style preset and
written to the output directory. Files are never overwritten — repeated
renders of the same molecule get `-1`, `-2`, … suffixes.

## Image options

| Option | Default | Description |
|--------|---------|-------------|
| Output Directory | `~/xyzrender-output` | Where images are saved |
| Image Format | SVG | SVG, PNG, PDF, or TIFF |
| Style Preset | default | One of xyzrender's 12 presets (see below) |
| Orientation | Avogadro view | Saved Avogadro camera, xyzrender auto-orientation, or raw coordinates |
| Canvas Size | 800 px | Raster output scales with this |
| Hydrogens | Preset default | Force all H shown or all H hidden |
| Transparent Background | off | Alpha instead of the preset background color |
| Label Atom Indices | off | Draw atom index labels |
| Label Stereochemistry | off | Annotate R/S, E/Z, axial, planar, helical |
| Show Non-Covalent Interactions | off | Dotted lines for hydrogen bonds and close contacts |

## Animation options

| Option | Default | Description |
|--------|---------|-------------|
| Output Directory | `~/xyzrender-output` | Where the GIF is saved |
| Rotation Axis | y | Axis the molecule rotates about |
| Style Preset | default | As above |
| Orientation | Avogadro view | As above |
| Canvas Size | 500 px | Large sizes make large GIF files |
| Frames per Second | 10 | Playback rate |
| Hydrogens | Preset default | As above |
| Transparent Background | off | As above |

## Style presets

`default`, `flat`, `paton`, `pmol`, `skeletal`, `bubble`, `vdw`, `tube`,
`mtube`, `btube`, `wire`, `graph`

## Notes

- **Orientation** defaults to *Avogadro view*, which reproduces the camera
  from the active view, so the render matches what is on screen. Only the
  rotation is reproduced — xyzrender renders orthographically, so a
  perspective projection is not. Avogadro sends the live camera to command
  scripts only in builds that carry that change; an older build falls back to
  the camera as of the last save, or to auto-orientation if the molecule has
  never been saved.
- Molecules with a unit cell render as crystals, with the cell box, ghost
  atoms, and axis arrows.
- Cubes and surfaces are not yet carried through the CJSON hand-off.

## Installation

```bash
cd avogadro-xyzrender
pixi install
```

Then register the plugin in Avogadro's Plugin Manager.

## Requirements

- Python ≥ 3.12
- [xyzrender](https://github.com/aligfellow/xyzrender) from `main` (installed
  automatically). CJSON support is not in a PyPI release yet, so the
  dependency points at the Git repository; `pixi.lock` pins the exact commit.

## License

BSD-3-Clause (xyzrender itself is MIT)
