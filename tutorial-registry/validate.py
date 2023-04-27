#!/usr/bin/env python
"""Validate tutorials' meta.yaml and generate an output directory with json/images to be uploaded on github pages."""
import argparse
import json
import shutil
from pathlib import Path
from typing import Dict, List

import jsonschema
import requests
import yaml
from PIL import Image

HERE = Path(__file__).absolute().parent


def _check_url_exists(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"URL {url} is not reachable (error {response.status_code}). ")


def _check_image(img_path):
    """Check that the image exists and that it is either SVG or fits into the 512x512 bounding box."""
    if not img_path.exists():
        raise ValueError(f"Image does not exist: {img_path}")
    if img_path.suffix != ".svg":
        with Image.open(img_path) as img:
            width, height = img.size
            if not ((width == 512 and height <= 512) or (width <= 512 and height == 512)):
                raise ValueError(
                    f"Image must fit in a 512x512px bounding box and one dimension must be exactly 512 px. Actual dimensions (width, height): ({width}, ({height}))."
                )


def validate_tutorials(schema_file: Path, tutorials_dir: Path):
    """Find all tutorial `meta.yaml` files in the tutorials dir and yield tutorial records."""
    with open(schema_file) as f:
        schema = json.load(f)

    for tmp_meta_file in tutorials_dir.glob("**/meta.yaml"):
        with open(tmp_meta_file) as f:
            tutorial_id = tmp_meta_file.parent.name
            tmp_tutorial = yaml.load(f, yaml.SafeLoader)
            jsonschema.validate(tmp_tutorial, schema)
            _check_url_exists(tmp_tutorial["link"])
            # replace image path by absolute local path to image
            img_path = tutorials_dir / tutorial_id / tmp_tutorial["image"]
            _check_image(img_path)
            tmp_tutorial["image"] = img_path
            yield tmp_tutorial


def load_categories(categories_file: Path):
    """Load the categories JSON."""
    with open(categories_file) as f:
        return yaml.load(f, yaml.SafeLoader)


def make_output_dir(categories: List[Dict], tutorials: List[Dict], outdir: Path):
    """Create the output directory.

    Structure:
    outdir
       - tutorials.json  # contains categories and tutorials
       - tutorialxxx/icon.svg  # original icon filenames under a folder for each tutorial. The path of the icon is listed in the json.
       - tutorialyyy/icon.png
    """
    outdir.mkdir(parents=True)

    for tutorial in tutorials:
        img_localpath = Path(tutorial["image"].parent.name) / tutorial["image"].name
        img_outpath = outdir / img_localpath
        img_outpath.parent.mkdir()
        shutil.copy(tutorial["image"], img_outpath)
        tutorial["image"] = str(img_localpath)

    result = {"categories": categories, "tutorials": tutorials}
    with open(outdir / "tutorials.json", "w") as f:
        json.dump(result, f)


def main(schema_file: Path, meta_dir: Path, categories_file: Path, outdir: Path):
    """Validate and create output directory."""
    tutorials = list(validate_tutorials(schema_file, meta_dir))
    categories = load_categories(categories_file)
    make_output_dir(categories, tutorials, outdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="Validate tutorials' meta.yaml and generate an output directory with json/images to be uploaded on github pages.",
    )
    parser.add_argument(
        "--outdir", help="outdir that will contain the data to be uploaded on github pages", required=True
    )
    args = parser.parse_args()

    outdir = Path(args.outdir)
    SCHEMA = HERE / "schema.json"
    META_DIR = HERE / "tutorials"
    CATEGORIES = HERE / "categories.yml"

    main(SCHEMA, META_DIR, CATEGORIES, outdir)
