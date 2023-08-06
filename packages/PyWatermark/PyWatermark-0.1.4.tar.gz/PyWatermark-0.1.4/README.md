## PyWatermark

A python library to watermark your images!

### Installation

`pip install PyWatermark`

### Features

This library exploits the usefulness of pillow to watermark images. It's an easy tool if you want to automate the watermarking of many images at once.

### Usage

```
from PyWatermark import waterMarkImages, getAvailableFonts

imageFile = "image.jpg"
imageOutputPath = "/Desktop" # write your output folder path here 
text = "Hello World" # Whatever text you want to watermark

# You can adjust the font here from the given fonts or just
# put in your own font path - a .ttf file
# Other parameters you can adjust are position, size, opacity
outFile = waterMarkImages(imageFile, imageOutputPath, text)

print(getAvailableFonts()) # prints out available fonts

```
### Contributing

Feel free to make suggestions, raise pull requests, and report issues. After all we're human and there can be problems with this library. Optimizing this is very appreciated.