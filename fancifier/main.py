import typer
import yaml
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
from rich.console import Console
from rich.progress import track

app = typer.Typer()
console = Console()


def enhance_grayscale(image):
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Adjust contrast
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.5)  # Adjust brightness
    return image


@app.command()
def generate_icons(color_file: Path, base_icon: Path, output_dir: Path):
    with open(color_file, "r") as f:
        colors = yaml.safe_load(f)["colors"]

    output_dir.mkdir(parents=True, exist_ok=True)
    base_image = Image.open(base_icon).convert("RGBA")
    grayscale_image = base_image.convert("L")
    grayscale_image = enhance_grayscale(grayscale_image)
    grayscale_image.show()

    console.print(
        f"[bold green]Generating icons for {len(colors)} colors...[/bold green]"
    )

    for color in track(colors, description="Processing..."):
        colored_image = change_icon_color(grayscale_image, color)
        # colored_image.show()
        icon_path = output_dir / f"icon_{color.lstrip('#')}.icns"
        save_icns(colored_image, icon_path)
        console.print(
            f"[bold blue]Saved icon for color {color} at {icon_path}[/bold blue]"
        )

    console.print("[bold green]Icon generation completed![/bold green]")


def change_icon_color(grayscale_image, hex_color):
    rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    colorized_image = ImageOps.colorize(grayscale_image, black="black", white=rgb_color)
    rgba_image = colorized_image.convert("RGBA")
    return rgba_image


def save_icns(image, path):
    image.save(path, format="ICNS")


if __name__ == "__main__":
    app()
