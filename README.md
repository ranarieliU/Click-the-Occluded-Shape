# Click-the-Occluded-Shape - Senior Project

##  what is medial axis
##  What this code does

## Usage example of PIL Image module
>>> import Image  
>>> im = Image.new('RGB', (512, 512), "white")  
>>> print(im.getpixel((1, 1))) # output: (255, 255, 255). this method is slow  
>>> pix = im.load()  
>>> print(pix[1, 1]) # output: (255, 255, 255). faster than getpixel  
>>> pix[1, 1] = (0, 0, 0) # set pixel to black  
>>> print(im.getpixel((1, 1))) # output: (0, 0, 0).  
>>> im.save("ran.bmp") # saves image in current directory  


