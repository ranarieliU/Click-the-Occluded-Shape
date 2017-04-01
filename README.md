# Click-the-Occluded-Shape - Senior Project

## Prerequisites
Use python 3
pip requirements are in: requirements.txt

### Analysis code usage:
python3 __main__.py

More info in: https://docs.google.com/document/d/1ncCIc6iYgPbueBj6SePr7RsNitWW7Zd4KMCjMO59SrU/edit

## Usage example of PIL Image module
>>> import Image  
>>> im = Image.new('RGB', (512, 512), "white")  
>>> print(im.getpixel((1, 1))) # output: (255, 255, 255). this method is slow  
>>> pix = im.load()  
>>> print(pix[1, 1]) # output: (255, 255, 255). faster than getpixel  
>>> pix[1, 1] = (0, 0, 0) # set pixel to black  
>>> print(im.getpixel((1, 1))) # output: (0, 0, 0).  
>>> im.save("test.bmp") # saves image in current directory


