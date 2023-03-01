import os
from PIL import Image, ImageChops


def slice(img_path, window_size, offset):
    try:
        img = Image.open(img_path)

        # Get the image width and height:
        width, height = img.size

        # Determine the window size in pixels if percents are given:
        if '%' in window_size:
            window_size = tuple(int(float(window_size.strip('%')) / i * 100) for i in img.size)

        # Check if window parameters are correct:
        if window_size[0] * window_size[1] > width or window_size[0] * window_size[1] > height:
            print('Invalid parameters for the window size. Window with this size is larger than the image.')

        # Create the save directory if it doesn't exist:
        save_dir = img_path.split('.')[0] + '_sliced'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Loop over the image and slice:
        for x in range(0, width - window_size[0] + 1, offset[0]):
            for y in range(0, height - window_size[1] + 1, offset[1]):
                # Give proper filename for the sliced parts:
                filename = os.path.join(save_dir,
                                        f"{img_path.split('/')[-1].split('.')[0]}"
                                        f"_{x}_{y}_{offset[0]}x{offset[1]}.png")
                # Slicing process:
                slice_img = img.crop((x, y, x + offset[0], y + offset[1]))
                slice_img.save(filename)

        # Closing the image:
        img.close()

    except FileNotFoundError:
        print('Image is not located in the directory')


def merge(path_to_slices):
    # Get all sliced images in the folder:
    try:
        sliced_images = sorted([os.path.join(path_to_slices, filename) for filename in os.listdir(path_to_slices)])

        # Open the original image:
        original_image_name = sliced_images[0].split('\\')[-1].split('_', 4)[0]
        files = os.listdir()
        for file in files:
            if file.startswith(original_image_name) and file.endswith(('jpg', 'jpeg', 'png')):
                image_path = os.path.join(file)
                original_img = Image.open(image_path)

        # Get the size of the original image and create a blank image with the correct size and mode:
        width, height = original_img.size
        original_mode = original_img.mode
        new_img = Image.new(original_mode, (width, height))

        # Loop over the sliced images and paste them into the new image to get merged image:
        for slice in sliced_images:
            # Open the sliced image:
            slice_img = Image.open(slice)
            # Determine the position in the blank image to put the sliced image:
            x = int(slice.split('\\')[-1].split('_', 3)[1])
            y = int(slice.split('\\')[-1].split('_', 3)[2])
            # Put the sliced images into the blank image:
            new_img.paste(slice_img, (x, y))

        # Verify that the merged image is the same as the original:
        diff = ImageChops.difference(original_img, new_img)
        if diff.getbbox():
            print("Merged image differs from the original. Check your window size please")
        else:
            print("Every pixel in the images is exactly the same")
            # Save the new image:
        new_img.save('merged.png')

        # Closing the images:
        original_img.close()
        new_img.close()

    except FileNotFoundError:
        print('There is no folder with the slices, try slice() function first')


# Run the example:
if __name__ == "__main__":
    slice('example.jpg', (20, 30), (100, 100))
    merge('example_sliced')






