import cv2
import numpy as np
from skimage import io


def color_transfer(source, target):
    # Convert the images from RGB to Lab color space
    source_lab = cv2.cvtColor(source, cv2.COLOR_RGB2LAB).astype("float32")
    target_lab = cv2.cvtColor(target, cv2.COLOR_RGB2LAB).astype("float32")

    # Compute the mean and standard deviation of each channel
    (l_mean_src, l_std_src, a_mean_src, a_std_src, b_mean_src, b_std_src) = (
        source_lab[:, :, 0].mean(),
        source_lab[:, :, 0].std(),
        source_lab[:, :, 1].mean(),
        source_lab[:, :, 1].std(),
        source_lab[:, :, 2].mean(),
        source_lab[:, :, 2].std(),
    )
    (l_mean_tar, l_std_tar, a_mean_tar, a_std_tar, b_mean_tar, b_std_tar) = (
        target_lab[:, :, 0].mean(),
        target_lab[:, :, 0].std(),
        target_lab[:, :, 1].mean(),
        target_lab[:, :, 1].std(),
        target_lab[:, :, 2].mean(),
        target_lab[:, :, 2].std(),
    )

    # Subtract the means from the target
    (l, a, b) = cv2.split(target_lab)
    l -= l_mean_tar
    a -= a_mean_tar
    b -= b_mean_tar

    # Scale by the standard deviations
    l = (l_std_src / l_std_tar) * l
    a = (a_std_src / a_std_tar) * a
    b = (b_std_src / b_std_tar) * b

    # Add in the source mean
    l += l_mean_src
    a += a_mean_src
    b += b_mean_src

    # Clip the pixel intensities to [0, 255] and convert back to uint8
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2RGB)

    return transfer


# Load the source (reference) and target (grayscale) images
source_image = io.imread("source_image.jpg")
target_image = io.imread("target_image.jpg")

# Apply color transfer
result_image = color_transfer(source_image, target_image)

# Display the results
io.imshow(result_image)
io.show()
