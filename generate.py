from pathlib import Path
import shutil
_clue_dir = Path("clues/")
_template_dir = Path("template/")
_site_dir = Path("site/")

def _generate_clue(clue_dir: Path, output_dir: Path):
    output_dir.mkdir(exist_ok=True, parents=True)
    
    text_f = clue_dir / "text.txt"
    text = text_f.read_text() if text_f.exists() else ""
    
    images = list(clue_dir.glob("image.*"))
    if images:
        image = images[0]
    else:
        image = _template_dir / "image.png"

    html = (_template_dir / "index.html").read_text().format(clue_text=text, img_url=image.name)
    (output_dir / "index.html").write_text(html)

    shutil.copy(_template_dir / "index.css", output_dir / "index.css")
    shutil.copy(image, output_dir / image.name)



def main():
    _generate_clue(_clue_dir / "1_cone", _site_dir / "sample_clue")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()

