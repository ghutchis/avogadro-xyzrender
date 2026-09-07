"""Render the current molecule to a publication-quality image using xyzrender."""

import json
import os
import tempfile

EXTENSIONS = {"SVG": ".svg", "PNG": ".png", "PDF": ".pdf", "TIFF": ".tiff"}

# "Orientation" option -> (load(camera=...), render(orient=...))
ORIENTATIONS = {
    "Avogadro view": (True, None),
    "Auto-orient": (False, True),
    "Raw coordinates": (False, False),
}


def run_render(avo_input):
    """Render a still image (SVG / PNG / PDF / TIFF)."""
    options = avo_input.get("options", {})
    setup = _prepare(avo_input, options)
    if "error" in setup:
        return setup

    extension = EXTENSIONS.get(str(options.get("format", "SVG")).upper(), ".svg")
    out_path = _unique_path(setup["output_dir"], setup["name"], extension)

    kwargs = {
        "config": options.get("style", "default"),
        "canvas_size": int(options.get("canvas_size", 800)),
        "transparent": bool(options.get("transparent", False)),
        "idx": bool(options.get("indices", False)),
        "stereo": bool(options.get("stereo", False)),
        "orient": setup["orient"],
        "output": out_path,
    }
    kwargs.update(_hydrogen_kwargs(options))

    from xyzrender import render

    try:
        render(setup["molecule"], **kwargs)
    except Exception as exc:
        return {"error": f"xyzrender failed to render the molecule: {exc}"}

    return {"message": f"Rendered image written to:\n\n{out_path}"}


def run_animation(avo_input):
    """Render a rotating animated GIF."""
    options = avo_input.get("options", {})
    setup = _prepare(avo_input, options)
    if "error" in setup:
        return setup

    out_path = _unique_path(setup["output_dir"], setup["name"], ".gif")

    kwargs = {
        "gif_rot": str(options.get("axis", "y")),
        "gif_fps": int(options.get("fps", 10)),
        "config": options.get("style", "default"),
        "canvas_size": int(options.get("canvas_size", 500)),
        "transparent": bool(options.get("transparent", False)),
        "orient": setup["orient"],
        "output": out_path,
    }
    kwargs.update(_hydrogen_kwargs(options))

    from xyzrender import render_gif

    try:
        render_gif(setup["molecule"], **kwargs)
    except Exception as exc:
        return {"error": f"xyzrender failed to render the animation: {exc}"}

    return {"message": f"Animation written to:\n\n{out_path}"}


def _prepare(avo_input, options):
    """Load the molecule from the CJSON Avogadro sent and create the output directory.

    CJSON is the native hand-off: xyzrender reads bond orders, per-atom colors,
    the unit cell, and a saved camera orientation from it, none of which survive
    a round trip through SDF.

    Returns a dict with "molecule", "name", "output_dir", and "orient", or an
    "error" key.
    """
    cjson = avo_input.get("cjson", {})
    numbers = cjson.get("atoms", {}).get("elements", {}).get("number", [])
    if not numbers:
        return {"error": "No molecule data received. Please open a molecule first."}

    output_dir = os.path.expanduser(options.get("output_dir", "~/xyzrender-output"))
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        return {"error": f"Could not create the output directory: {exc}"}

    name = str(cjson.get("name", "")).strip() or "molecule"
    # sanitize for use as a file name
    name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)

    camera, orient = ORIENTATIONS.get(
        options.get("orientation", "Avogadro view"), (True, None)
    )

    # xyzrender reads from a file, so write the CJSON to a temporary one
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".cjson", prefix=name + "_", delete=False
    ) as tmp:
        tmp_path = tmp.name
        json.dump(cjson, tmp)

    from xyzrender import load

    try:
        molecule = load(
            tmp_path,
            charge=int(avo_input.get("charge", 0)),
            multiplicity=int(avo_input.get("spin", 1)),
            nci_detect=bool(options.get("nci", False)),
            camera=camera,
        )
    except Exception as exc:
        return {"error": f"xyzrender could not parse the molecule: {exc}"}
    finally:
        os.unlink(tmp_path)

    return {
        "molecule": molecule,
        "name": name,
        "output_dir": output_dir,
        "orient": orient,
    }


def _hydrogen_kwargs(options):
    """Translate the hydrogen display option into render() keyword arguments."""
    choice = options.get("hydrogens", "Preset default")
    if choice == "Show all":
        return {"hy": True}
    if choice == "Hide all":
        return {"no_hy": True}
    return {}


def _unique_path(directory, stem, extension):
    """Return a path in directory that does not overwrite an existing render."""
    path = os.path.join(directory, stem + extension)
    counter = 1
    while os.path.exists(path):
        path = os.path.join(directory, f"{stem}-{counter}{extension}")
        counter += 1
    return path
