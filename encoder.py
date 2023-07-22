#!/usr/bin/python
from PIL import Image
import numpy as np 

with open('shellcode.txt', 'r') as shellcode:
    shellcode_as_text_test = shellcode.read().rstrip().replace('\n','')
    print(shellcode_as_text_test)


def text_to_binary(text_data):
    # Convert text data to binary format
    return ''.join(format(ord(char), '08b') for char in text_data)

def encode_lsb(image_path, plaintext_data, output_path):
    image = Image.open(image_path)
    
    # Convert the image to RGB mode (if it's not already)
    image = image.convert("RGB")

    width, height = image.size
    max_data_length = (width * height) * 3  # 3 channels (RGB) per pixel

    # Convert plaintext to binary format
    binary_data = text_to_binary(plaintext_data)

    # Append a special character to mark the end of the data
    binary_data += "00000000"  # Null character '\0'

    # Check if the data can fit into the image
    data_length = len(binary_data)
    if data_length > max_data_length:
        raise ValueError("Data too large for the image.")

    # Create a copy of the image to modify
    encoded_image = image.copy()
    binary_index = 0

    # Embed binary data into the image using LSB steganography
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for channel in range(3):  # 3 channels (RGB)
                if binary_index < len(binary_data):
                    # Modify the least significant bit of the pixel
                    pixel[channel] = pixel[channel] & ~1 | int(binary_data[binary_index])
                    binary_index += 1
                else:
                    break
            encoded_image.putpixel((x, y), tuple(pixel))

    # Save the encoded image
    encoded_image.save(output_path)
    print("Data encoded and image saved successfully.")

# Example usage:
if __name__ == "__main__":
    image_path = "example.png"

    encode_lsb(image_path, shellcode_as_text_test, f"poc_{image_path}")
