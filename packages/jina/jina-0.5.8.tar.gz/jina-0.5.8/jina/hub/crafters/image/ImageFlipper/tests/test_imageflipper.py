import numpy as np

from .. import ImageFlipper


def create_random_img_array(img_height, img_width):
    import numpy as np
    return np.random.randint(0, 256, (img_height, img_width, 3))


def test_horizontal_flip():
    img_size = 217
    crafter = ImageFlipper()
    # generates a random image array of size (217, 217)
    img_array = create_random_img_array(img_size, img_size)
    crafted_chunk = crafter.craft(img_array)
    # image flips along the second axis (horizontal flip)
    flip_img_array = np.fliplr(img_array)
    # assert flipped image using numpy's fliplr method
    np.testing.assert_equal(crafted_chunk['blob'], flip_img_array)


def test_vertical_flip():
    img_size = 217
    crafter = ImageFlipper(vertical=True)
    # generates a random image array of size (217, 217)
    img_array = create_random_img_array(img_size, img_size)
    crafted_chunk = crafter.craft(img_array)
    # image flips along the first axis (vertical flip)
    flip_img_array = np.flipud(img_array)
    # assert flipped image using numpy's flipud method
    np.testing.assert_equal(crafted_chunk['blob'], flip_img_array)
