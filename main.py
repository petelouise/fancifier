import os
from pathlib import Path
import click
import yaml
from PIL import Image, ImageOps


@click.command()
@click.option(
    "--color-file",
    required=True,
    type=click.Path(exists=True),
    help="YAML file with list of colors.",
)
@click.option(
    "--base-icon",
    required=True,
    type=click.Path(exists=True),
    help="Path to the base icon image.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(),
    help="Directory to save the generated icons.",
)
def generate_icons(color_file, base_icon, output_dir):
    # Load colors from the YAML file
    with open(color_file, "r") as f:
        colors = yaml.safe_load(f)["colors"]

    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the base icon image
    base_image = Image.open(base_icon).convert("RGBA")

    for color in colors:
        # Create a colored version of the base icon
        colored_image = change_icon_color(base_image, color)

        # Save the colored icon as .icns
        icon_path = output_dir / f"icon_{color.lstrip('#')}.icns"
        save_icns(colored_image, icon_path)


def change_icon_color(base_image, color):
    # Create a new image with the specified color
    color_image = Image.new("RGBA", base_image.size, color)

    # Composite the base image with the color image
    combined_image = Image.alpha_composite(color_image, base_image)

    return combined_image


def save_icns(image, path):
    # Save image as .icns
    image.save(path, format="ICNS")


if __name__ == "__main__":
    generate_icons()
