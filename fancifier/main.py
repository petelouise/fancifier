from pathlib import Path

import typer
import yaml
from PIL import Image, ImageEnhance
from rich.console import Console
from rich.progress import track

app = typer.Typer()
console = Console()


@app.command()
def generate_icons(color_file: Path, base_icon: Path, output_dir: Path):
    # Load colors from the YAML file
    with open(color_file, "r") as f:
        colors = yaml.safe_load(f)["colors"]

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the base icon image
    base_image = Image.open(base_icon).convert("RGBA")

    console.print(
        f"[bold green]Generating icons for {len(colors)} colors...[/bold green]"
    )

    for color in track(colors, description="Processing..."):
        # Create a colored version of the base icon
        colored_image = change_icon_color(base_image, color)

        # Save the colored icon as .icns
        icon_path = output_dir / f"icon_{color.lstrip('#')}.icns"
        save_icns(colored_image, icon_path)
        console.print(
            f"[bold blue]Saved icon for color {color} at {icon_path}[/bold blue]"
        )

    console.print("[bold green]Icon generation completed![/bold green]")


def change_icon_color(base_image, hex_color):
    # Convert hex color to RGB
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))

    # Desaturate the image
    enhancer = ImageEnhance.Color(base_image)
    desaturated_image = enhancer.enhance(0)

    # Create a new image with the target color
    color_overlay = Image.new("RGBA", base_image.size, (r, g, b, 255))

    # Composite the color overlay with the desaturated image using the original alpha channel
    new_image = Image.composite(color_overlay, desaturated_image, base_image.split()[3])

    return new_image


def save_icns(image, path):
    # Save image as .icns
    image.save(path, format="ICNS")


if __name__ == "__main__":
    app()
