from PIL import Image


# Convert binary pixel data to an image, supporting any dimensions
def binary_to_image(binary_data, output_file):
    if not binary_data:
        print("No binary data provided.")
        return

    # Ensure all rows have the same length (consistent width)
    width = len(binary_data[0])  # Get width from the first row
    height = len(binary_data)  # Number of rows defines the height

    # Check for any inconsistent row lengths
    for row in binary_data:
        if len(row) != width:
            print("Error: Inconsistent row lengths found in the binary data.")
            return

    # Create a new black-and-white (1-bit pixels) image
    image = Image.new("1", (width, height))

    # Load the image's pixel data
    pixels = image.load()

    # Convert the binary data into pixel values (1 = white, 0 = black)
    for y, row in enumerate(binary_data):
        for x, value in enumerate(row):
            pixels[x, y] = int(value)

    # Save the image
    image.save(output_file)
    print(f"Image saved as {output_file}")
