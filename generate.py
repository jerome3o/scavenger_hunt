from pathlib import Path
import shutil

from typing import Optional

import hashlib
from pydantic import BaseModel
import jinja2


clue_number_fixup = {
    "1_cone": 1,
    "2_mailbox": 2,
    "3_park_bench_map": 3,
    "5_bridge": 5,
    "6_book_buoy": 6,
    "4_seagull": 4,
    "7_placeholder": 7,  # telescope
    "8_placeholder": 8,  # rock
    "9_placeholder": 9,  # DVD
    "10_placeholder": 10,  # final
}


class Clue(BaseModel):
    encoded_name: str
    name: str
    number: int
    text: Optional[str] = None
    image_path: Optional[str] = None
    image_uri: Optional[str] = None


def render_clue(clue: Clue, total: int):
    # Set up the Jinja2 environment
    template_loader = jinja2.FileSystemLoader(searchpath="./jinja_templates/")
    template_env = jinja2.Environment(loader=template_loader)
    # Load the template
    template = template_env.get_template("clue.html")

    # Render the template with the context
    output = template.render(**clue.dict(), total=total)

    return output


def render_clue_index(clues: dict):
    # Set up the Jinja2 environment
    template_loader = jinja2.FileSystemLoader(searchpath="./jinja_templates/")
    template_env = jinja2.Environment(loader=template_loader)

    # Load the template
    template = template_env.get_template("clue_index.html")

    # Render the template with the context
    output = template.render(clues=clues)

    return output


def load_clue_data(clue_dir: Path) -> Clue:

    name: str = clue_dir.name
    encoded_name: str = _get_encoded_name(name)

    # get clue number by splitting on _ and getting the first part
    clue_number = clue_number_fixup[name]

    # load clue text from text.txt, if it exists
    text = (clue_dir / "text.txt").read_text() if (clue_dir / "text.txt").exists() else ""

    # load image if there is a file with the word "image" in the name
    image_path = next(clue_dir.glob("*image*"), None)
    image_uri = None
    if image_path is not None:
        image_uri = f"/scavenger_hunt/images/{name}{image_path.suffix}" if image_path else ""
        image_path = str(image_path)

    return Clue(
        text=text,
        number=clue_number,
        image_path=image_path,
        image_uri=image_uri,
        name=name,
        encoded_name=encoded_name,
    )


def load_clues_from_clue_dir(clue_dirs: Path) -> dict:
    clues = {}
    for clue_dir in clue_dirs.iterdir():

        if not clue_dir.is_dir():
            continue

        # check if dir is empty
        if not list(clue_dir.iterdir()):
            continue

        clues[clue_dir.name] = load_clue_data(clue_dir)

    return clues


def _get_encoded_name(name: str) -> str:
    return str(hashlib.sha256(name.encode("utf-8")).hexdigest())


def main():
    # load clues
    clues = load_clues_from_clue_dir(Path("clues"))

    # copy clue images to site/scavenger_hunt/images
    for clue in clues.values():
        if clue.image_path:
            print(f"Copying {clue.image_path} to site/scavenger_hunt/images")
            output_path = Path("site" + clue.image_uri)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(Path(clue.image_path).read_bytes())

    # render clues
    for name, clue in clues.items():
        output = render_clue(clue, len(clues))
        path = Path("site") / "scavenger_hunt" / f"{clue.encoded_name}" / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        print("Saving clue", name, "to", path)
        path.write_text(output)

    # render the clue page and save it
    output = render_clue_index(sorted(clues.values(), key=lambda clue: clue.number))
    path = Path("site") / "scavenger_hunt" / "clue_index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    print("Saving clue index to", path)
    path.write_text(output)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
