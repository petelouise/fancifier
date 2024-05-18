import cv2
import numpy as np
from skimage import io, color
import matplotlib.pyplot as plt


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def apply_color_map(image, colormap="viridis"):
    colormaps = {
        "viridis": plt.cm.viridis,
        "plasma": plt.cm.plasma,
        "inferno": plt.cm.inferno,
        "magma": plt.cm.magma,
        "cividis": plt.cm.cividis,
    }
    if colormap not in colormaps:
        raise ValueError(
            f"Colormap '{colormap}' is not supported. Choose from {list(colormaps.keys())}."
        )
    return colormaps[colormap](image)


def colorize_image(image_path, hex_color):
    # Read the grayscale image
    gray_image = io.imread(image_path, as_gray=True)

    # Apply the colormap
    colored_image = apply_color_map(gray_image)

    # Convert the colored image to uint8
    colored_image = (colored_image[:, :, :3] * 255).astype("uint8")

    return colored_image


def adjust_image_colors(image, hex_color):
    # Convert the hex color to RGB
    rgb_color = hex_to_rgb(hex_color)

    # Convert the colorized image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Adjust the hue to match the given hex color
    hsv[:, :, 0] = rgb_color[0]
    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.5)  # Increase saturation
    hsv[:, :, 2] = cv2.multiply(hsv[:, :, 2], 1.2)  # Increase brightness

    # Convert back to RGB color space
    adjusted_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    return adjusted_image


def colorize_and_adjust(image_path, hex_color, colormap="viridis"):
    colored_image = colorize_image(image_path, hex_color)
    adjusted_image = adjust_image_colors(colored_image, hex_color)
    return adjusted_image


def save_image(image, output_path):
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))


# Example usage:
if __name__ == "__main__":
    input_image_path = "grayscale_image.jpg"
    output_image_path = "adjusted_colorized_image.jpg"
    hex_color = "#FF5733"

    result_image = colorize_and_adjust(input_image_path, hex_color)
    save_image(result_image, output_image_path)
