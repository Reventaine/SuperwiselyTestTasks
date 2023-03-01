import os
import cv2
from PIL import Image


def composite():
    masks = sorted(os.listdir("DAVIS/Annotations/480p/"))
    originals = sorted(os.listdir("DAVIS/JPEGImages/480p/"))

    for i, j in zip(masks, originals):
        # Set the dataset path:
        masks_path = f"DAVIS/Annotations/480p/{i}"
        originals_path = f"DAVIS/JPEGImages/480p/{j}"

        # Set the output directory path:
        output_dir = f"DAVIS/CompositeImages/{i}"

        # Create the output directory if it doesn't exist:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get a list of all the files in the input directories:
        files_1 = sorted(os.listdir(masks_path))
        files_2 = sorted(os.listdir(originals_path))

        # Iterate over the files in the input directories and composite the images:
        for file_1, file_2 in zip(files_1, files_2):
            # Load the mask image:
            mask_image_path = os.path.join(masks_path, file_1)
            mask_image = Image.open(mask_image_path).convert("RGB")

            # Load the original image:
            original_image_path = os.path.join(originals_path, file_2)
            original_image = Image.open(original_image_path).convert('RGB')

            # Composite the images:
            result = Image.blend(mask_image, original_image, 0.5)

            # Save the resulting image:
            output_path = os.path.join(output_dir, file_1[:-4] + ".jpg")
            result.save(output_path)

            # Closing images:
            mask_image.close()
            original_image.close()


def main():
    # Create composite images for annotations and original frames if not exists:
    if not os.path.exists("DAVIS/CompositeImages/"):
        composite()

    # Define the output video dimensions:
    output_width = 910
    output_height = 480

    # Create a VideoWriter object to save the output video:
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("output.avi", fourcc, 30.0, (output_width, output_height))

    # Iterate over the videos and add them to the output video:
    for i in sorted(os.listdir("DAVIS/CompositeImages")):
        # Load the frames for the current video:
        frames_path = f"DAVIS/CompositeImages/{i}"
        frames = sorted(os.listdir(f"DAVIS/CompositeImages/{i}"))

        # Iterate over the frames and add them to the output video:
        for j in range(len(frames)):
            # Load the current frame:
            frame = cv2.imread(os.path.join(frames_path, frames[j]))
            # Resize the frame to the desired size:
            frame = cv2.resize(frame, (output_width, output_height))
            # Write the frame to the output video:
            out.write(frame)

    # Release the output video:
    cv2.destroyAllWindows()
    out.release()


if __name__ == "__main__":
    main()




