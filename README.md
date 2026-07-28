# avogadro-xyzrender

Publication-quality molecular graphics from Avogadro 2 using
[xyzrender](https://github.com/aligfellow/xyzrender).

Adds two items to **File → Export**:

- **Rendered Image (xyzrender)...** — a still SVG, PNG, PDF, or TIFF
- **Rendered Animation (xyzrender)...** — a rotating animated GIF

The current molecule is passed to xyzrender as an SDF (so Avogadro's bond
orders are used), rendered with the chosen style preset, and written to the
output directory. Files are never overwritten — repeated renders of the same
molecule get `-1`, `-2`, … suffixes.

## Image options

| Option | Default | Description |
|--------|---------|-------------|
| Output Directory | `~/xyzrender-output` | Where images are saved |
| Image Format | SVG | SVG, PNG, PDF, or TIFF |
| Style Preset | default | One of xyzrender's 12 presets (see below) |
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
| Canvas Size | 500 px | Large sizes make large GIF files |
| Frames per Second | 10 | Playback rate |
| Hydrogens | Preset default | As above |
| Transparent Background | off | As above |

## Style presets

`default`, `flat`, `paton`, `pmol`, `skeletal`, `bubble`, `vdw`, `tube`,
`mtube`, `btube`, `wire`, `graph`

## Notes

- Orientation is chosen by xyzrender's auto-orientation, not by Avogadro's
  current camera — the render will not necessarily match the view on screen.
- Only the molecule is exported. Unit cells, cubes, and surfaces present in
  Avogadro are not carried through the SDF hand-off.

## Installation

```bash
cd avogadro-xyzrender
pixi install
```

Then register the plugin in Avogadro's Plugin Manager.

## Requirements

- Python ≥ 3.12
- [xyzrender](https://pypi.org/project/xyzrender/) ≥ 0.3.8 (installed automatically)

## License

BSD-3-Clause (xyzrender itself is MIT)
