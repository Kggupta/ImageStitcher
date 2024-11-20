from PIL import Image
import sys, os
imageTypes = [".png", ".jpg", ".jpeg"]

if len(sys.argv) != 3:
    raise Exception("Requires Root Directory and output file name.\n- Example: python3 stitch.py ./rootdir/ outputFileName.png")

rootDirectory = sys.argv[1]
outputFileName = sys.argv[2]

def isAnImageSimple(name):
    """
    Returns if the name is an image type. Very simple implementation, doesn't need
    to be more complicated for this purpose.
    :param name: The name of the file
    :return: Whether it's an image name
    """
    for suffix in imageTypes:
        if name.endswith(suffix):
            return True
    return False

def concatHorizontal(left, right):
    """
    Merge two Pillow image objects together horizontally. Keeps the height dimension of left image.
    :param left: The image to place on the left
    :param right: The image to place on the right
    :return: The new concatenated image with left:right
    """

    # Handle Initial Case when no left image yet.
    if left is None:
        return right

    # create a new image with dimensions to fit left and right
    newImage = Image.new('RGB', (left.width + right.width, left.height))

    # place the left and right image into the blank image
    newImage.paste(left, (0, 0))
    newImage.paste(right, (left.width, 0))

    # send back the new image
    return newImage


def concatVertical(top, bottom):
    """
    Merge two Pillow image objects together vertically. Keeps the width dimension of top image.
    :param top: The image to place on the top
    :param bottom: The image to place on the bottom
    :return: The new concatenated image with top over bottom.
    """

    # Initial case when top is empty
    if top is None:
        return bottom

    # Create blank image canvas with correct dimensions
    newImage = Image.new('RGB', (top.width, top.height + bottom.height))

    # Place images on canvas
    newImage.paste(top, (0, 0))
    newImage.paste(bottom, (0, top.height))
    return newImage


def buildColumn(directory):
    """
    Places all image files in the directory in a single column. Top = alphanumerically smallest, Bottom = alphanumerically largest
    :param directory: The directory to build the column with
    :return: The entire column image object using the images that were in the given directory
    """

    # Get all files in the directory
    allImageNamesInColumn = [x for x in os.listdir(directory) if os.path.isfile(os.path.join(directory, x))]

    # Sort alphanumerically
    allImageNamesInColumn.sort()

    column = None
    # For every image in the directory
    for imgName in allImageNamesInColumn:
        # Only process images
        if isAnImageSimple(imgName):
            # Add the next image to the column
            column = concatVertical(column, Image.open(os.path.join(directory, imgName)))
    return column


def buildImage(rootDir):
    """
    Builds the entire image using the root directory
    :param rootDir: The directory to start searching for columns
    :return: Save the image with the specified output name in command line arguments
    """

    # Get all directories in the root directory
    allDirectories = [x[0] for x in os.walk(rootDir)]
    # Sort them alphanumerically
    allDirectories.sort()
    # Remove the rootDirectory itself
    allDirectories.pop(0)

    fullImage = None
    # Build the image column by column
    for dirName in allDirectories:
        # Build a new column
        newColumn = buildColumn(dirName)
        # Add the column to the right of the fullImage
        fullImage = concatHorizontal(fullImage, newColumn)

    # Save the image to your computer
    fullImage.save(outputFileName)

# Just some status indicators since it can take a long time
# If the input contains large images.
print(f"Building image using the provided information.\n- Directory: {rootDirectory}\n- Output: {outputFileName}")
print("\nPlease wait... ", end="")
buildImage(rootDirectory)
print("Success.")
