"""Render the current molecule to a publication-quality image using xyzrender."""

import os
import tempfile

EXTENSIONS = {"SVG": ".svg", "PNG": ".png", "PDF": ".pdf", "TIFF": ".tiff"}


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
    """Load the molecule from the SDF Avogadro sent and create the output directory.

    Returns a dict with "molecule", "name", and "output_dir", or an "error" key.
    """
    sdf_content = avo_input.get("sdf", "")
    if not sdf_content.strip():
        return {"error": "No molecule data received. Please open a molecule first."}

    output_dir = os.path.expanduser(options.get("output_dir", "~/xyzrender-output"))
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        return {"error": f"Could not create the output directory: {exc}"}

    cjson = avo_input.get("cjson", {})
    name = cjson.get("name", "").strip() or _name_from_sdf(sdf_content) or "molecule"
    # sanitize for use as a file name
    name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)

    # xyzrender reads from a file, so write the SDF to a temporary one
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".sdf", prefix=name + "_", delete=False
    ) as tmp:
        tmp_path = tmp.name
        tmp.write(sdf_content)

    from xyzrender import load

    try:
        molecule = load(
            tmp_path,
            charge=int(avo_input.get("charge", 0)),
            multiplicity=int(avo_input.get("spin", 1)),
            nci_detect=bool(options.get("nci", False)),
        )
    except Exception as exc:
        return {"error": f"xyzrender could not parse the molecule: {exc}"}
    finally:
        os.unlink(tmp_path)

    return {"molecule": molecule, "name": name, "output_dir": output_dir}


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


def _name_from_sdf(sdf_content: str) -> str:
    """Extract the molecule name from the first line of an SDF/MOL block."""
    first_line = sdf_content.splitlines()[0].strip() if sdf_content else ""
    return first_line if first_line else ""
