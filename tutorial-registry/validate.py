#!/usr/bin/env python
"""Validate tutorials' meta.yaml and generate an output directory with json/images to be uploaded on github pages."""

from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Literal, cast

import httpx
import jsonschema
import yaml
from PIL import Image

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, ValuesView

    Tutorial = Mapping[str, str | Iterable[str]]

HERE = Path(__file__).absolute().parent


async def _check_url_exists(client: httpx.AsyncClient, url: str) -> None:
    response = await client.head(url)
    if response.status_code != 200:
        raise ValueError(f"URL {url} is not reachable (error {response.status_code}). ")


def _check_image(img_path: Path) -> None:
    """Check that the image exists and that it is either SVG or fits into the 512x512 bounding box."""
    if not img_path.exists():
        raise ValueError(f"Image does not exist: {img_path}")
    if img_path.suffix == ".svg":
        return
    with Image.open(img_path) as img:
        width, height = img.size
    if not ((width == 512 and height <= 512) or (width <= 512 and height == 512)):
        raise ValueError(
            dedent(
                f"""\
                When validating {img_path}: Image must fit in a 512x512px bounding box and one dimension must be
                exactly 512 px. Actual dimensions (width, height): ({width}, ({height}))."
                """
            )
        )


async def validate_tutorials(schema_file: Path, tutorials_dir: Path) -> ValuesView[Tutorial]:
    """Find all tutorial `meta.yaml` files in the tutorials dir and yield tutorial records."""
    schema = json.loads(schema_file.read_bytes())
    known_links: dict[str, Tutorial] = {}
    known_primary_to_orders: dict[str, set[int]] = {}

    for tmp_meta_file in tutorials_dir.rglob("meta.yaml"):
        tutorial_id = tmp_meta_file.parent.name
        with tmp_meta_file.open() as f:
            tmp_tutorial = cast("Tutorial", yaml.load(f, yaml.SafeLoader))

        jsonschema.validate(tmp_tutorial, schema)

        if (link := tmp_tutorial["link"]) in known_links:
            raise ValueError(f"When validating {tmp_meta_file}: Duplicate link: {link}")
        known_links[link] = tmp_tutorial

        # Check for duplicate orders within the same primary category
        primary_category = tmp_tutorial.get("primary_category")
        order = tmp_tutorial.get("order")

        if primary_category and order is not None:
            if primary_category not in known_primary_to_orders:
                known_primary_to_orders[primary_category] = set()

            if order in known_primary_to_orders[primary_category]:
                raise ValueError(
                    f"When validating {tmp_meta_file}: Duplicate order {order} "
                    f"for primary category '{primary_category}'"
                )

            known_primary_to_orders[primary_category].add(order)

        # replace image path by absolute local path to image
        img_path = tutorials_dir / tutorial_id / tmp_tutorial["image"]
        _check_image(img_path)
        tmp_tutorial["image"] = str(img_path)

    headers = {"User-Agent": "scverse tutorial registry (https://github.com/scverse/scverse-tutorials)"}
    async with httpx.AsyncClient(headers=headers) as client, asyncio.TaskGroup() as tg:
        for link in known_links:
            tg.create_task(_check_url_exists(client, link))

    return known_links.values()


def load_categories(categories_file: Path) -> dict[str, Any]:
    """Load the categories JSON."""
    with open(categories_file) as f:
        return yaml.load(f, yaml.SafeLoader)


def make_output(
    categories: Iterable[Mapping[str, Mapping[Literal["description"], str]]],
    tutorials: Iterable[Tutorial],
    *,
    outdir: Path | None = None,
) -> None:
    """Create the output directory.

    Structure:
    outdir
       - tutorials.json  # contains categories and tutorials
       - tutorialxxx/icon.svg  # original icon filenames under a folder for each tutorial. The path of the icon is listed in the json.
       - tutorialyyy/icon.png
    """
    if outdir:
        outdir.mkdir(parents=True)

    tutorials_rel = []
    for tutorial in tutorials:
        img_srcpath = Path(tutorial["image"])
        img_localpath = Path(img_srcpath.parent.name) / img_srcpath.name
        tut_rel = dict(tutorial)
        tut_rel["image"] = str(img_localpath)
        tutorials_rel.append(tut_rel)
        if outdir:
            img_outpath = outdir / img_localpath
            img_outpath.parent.mkdir()
            shutil.copy(img_srcpath, img_outpath)

    result = {"categories": categories, "tutorials": tutorials_rel}

    if outdir:
        with (outdir / "tutorials.json").open("w") as f:
            json.dump(result, f)
    else:
        json.dump(result, sys.stdout, indent=2)


def main(schema_file: Path, meta_dir: Path, categories_file: Path, *, outdir: Path | None = None) -> None:
    """Validate and create output directory."""
    tutorials = asyncio.run(validate_tutorials(schema_file, meta_dir))
    categories = load_categories(categories_file)
    make_output(categories, tutorials, outdir=outdir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="Validate tutorials' meta.yaml and generate an output directory with json/images to be uploaded on github pages.",
    )
    parser.add_argument("--outdir", type=Path, help="outdir that will contain the data to be uploaded on github pages")
    args = parser.parse_args()

    SCHEMA = HERE / "schema.json"
    META_DIR = HERE / "tutorials"
    CATEGORIES = HERE / "categories.yml"

    main(SCHEMA, META_DIR, CATEGORIES, outdir=args.outdir)
