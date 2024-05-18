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

    # Split the image into RGBA channels
    r_channel, g_channel, b_channel, a_channel = base_image.split()

    # Create new RGB channels with the target color
    r_channel = r_channel.point(lambda _: r)
    g_channel = g_channel.point(lambda _: g)
    b_channel = b_channel.point(lambda _: b)

    # Merge the new RGB channels with the original alpha channel
    new_image = Image.merge("RGBA", (r_channel, g_channel, b_channel, a_channel))

    return new_image


def save_icns(image, path):
    # Save image as .icns
    image.save(path, format="ICNS")


if __name__ == "__main__":
    app()
