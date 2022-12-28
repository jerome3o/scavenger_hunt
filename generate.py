from pathlib import Path
import shutil
import qrcode
from urllib.parse import quote_plus
import base64
import hashlib

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

_clue_dir = Path("clues/")
_template_dir = Path("template/")
_site_dir = Path("site/")
_qr_dir = Path("qrcodes/")
_base_url = "https://kuaochella.com/scavenger_hunt/"
# _base_url = "http://192.168.1.23:8000/scavenger_hunt/"


def _generate_clue(
    clue_dir: Path,
    output_dir: Path,
):
    output_dir.mkdir(exist_ok=True, parents=True)

    text_f = clue_dir / "text.txt"
    text = text_f.read_text() if text_f.exists() else ""

    images = list(clue_dir.glob("image.*"))
    image = None
    if images:
        image = images[0]
        img_text = f'<img src="{image.name}" alt="oops!" class="center"/>'
    else:
        img_text = ""

    html = (_template_dir / "index.html").read_text().format(clue_text=text, img_text=img_text)
    (output_dir / "index.html").write_text(html)

    shutil.copy(
        _template_dir / "index.css",
        output_dir / "index.css",
    )
    if image:
        shutil.copy(image, output_dir / image.name)


def _generate_qr_code(fn: str, url: str, text: str):
    # # qr code
    raw_img = qrcode.make(data=url)
    text_pad = 100
    img = Image.new(raw_img.mode, size=(raw_img.size[0], raw_img.size[1] + text_pad), color=255)
    img.putdata(raw_img.getdata())

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 18)
    draw.text((20, raw_img.size[1] + text_pad // 2), text, font=font)

    img.save(fn)


def _get_encoded_name(name: str) -> str:
    return str(hashlib.sha256(name.encode("utf-8")).hexdigest())


# takes in a list of 4 pil images and collates them into a 2x2 image
def _collate_images(images: list, output_fn: str):
    assert len(images) == 4
    width = images[0].size[0]
    height = images[0].size[1]
    img = Image.new("RGB", (width * 2, height * 2), color="white")
    for i, image in enumerate(images):
        img.paste(image, (i % 2 * width, i // 2 * height))
    img.save(output_fn)


def main():
    _qr_dir.mkdir(exist_ok=True, parents=True)

    for clue_dir in _clue_dir.iterdir():
        if not list(clue_dir.iterdir()):
            continue
        clue_title = clue_dir.name
        clue_encoded_title = _get_encoded_name(clue_title)
        _generate_clue(
            clue_dir,
            _site_dir / "scavenger_hunt" / clue_encoded_title,
        )
        _generate_qr_code(
            _qr_dir / f"{clue_title}.png",
            (_base_url + clue_encoded_title).encode("utf-8"),
            clue_title,
        )

    clue_dirs = sorted(d.stem for d in Path(_clue_dir).iterdir() if d.is_dir())
    html = "<html>\n<body>\n<ul>\n"
    for folder in clue_dirs:
        encoded_name = _get_encoded_name(folder)
        html += f"<li><a href='/scavenger_hunt/{encoded_name}'>{folder}</a></li>\n"
    html += "</ul>\n</body>\n</html>"

    Path("site/scavenger_hunt/clue_index.html").write_text(html)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
