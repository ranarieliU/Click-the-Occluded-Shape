from PIL import Image
from os import listdir
import os
from os.path import isfile, join


def save_image(path, image):
    image.save(path)


def read_image(path):
    im = Image.open(path)
    rgb_im = im.convert('RGB')
    return rgb_im


# utility func for calc_boundaries
def is_boundary(image, coord):
    # print(coord)
    width, height = image.size
    x, y = coord
    r, g, b = image.getpixel((x, y))
    if r > 245 and g > 245 and b > 245:
        return False
    if x == 0 or y == 0 or x == width - 1 or y == height - 1:
        return True
    try:
        right = image.getpixel((x - 1, y))
        left = image.getpixel((x + 1, y))
        up = image.getpixel((x, y - 1))
        down = image.getpixel((x, y + 1))
    except:
        print((x, width - 1))
        print((x + 1, y))
    r, g, b = right
    if (r is not 191 or g is not 191 or b is not 191):
        if (r is not 255 or g is not 255 or b is not 255):
            print(right)
        return True
    r, g, b = left
    if (r is not 191 or g is not 191 or b is not 191):
        if (r is not 255 or g is not 255 or b is not 255):
            print(left)
        return True
    r, g, b = up
    if (r is not 191 or g is not 191 or b is not 191):
        if (r is not 255 or g is not 255 or b is not 255):
            print(up)
        return True
    r, g, b = down
    if (r is not 191 or g is not 191 or b is not 191):
        if (r is not 255 or g is not 255 or b is not 255):
            print(down)
        return True
    return False


# will get an image that has been read as param, will return a list of (X,Y) coordinates that are the image boundaries
def calc_boundaries(image):
    ans = []
    width, height = image.size
    for i in range(height):
        for j in range(width):
            if is_boundary(image, (j, i)):
                ans.append((j, i))
    return ans


def fix_image(image):
    width, height = image.size
    pixels = image.load()
    for i in range(height):
        for j in range(width):
            r, g, b = image.getpixel((j, i))
            if r < 235 or g < 235 or b < 235:
                pixels[j, i] = (191, 191, 191)
            else:
                pixels[j, i] = (255, 255, 255)
    return image


def whiten(image):
    pixels = image.load()
    width, height = image.size
    for i in range(height):
        for j in range(width):
            curr_color = pixels[j, i]
            if curr_color[0] < 255 and curr_color[0] > 0:
                pixels[j, i] = (255, 255, 255)
    return image


def replace_white_and_black(image):
    pixels = image.load()
    width, height = image.size
    for i in range(height):
        for j in range(width):
            curr_color = pixels[j, i]
            if curr_color[0] == 0:
                pixels[j, i] = (255, 255, 255)
            elif curr_color[0] == 255:
                pixels[j, i] = (0, 0, 0)
    return image


def mark_boundary(image, boundaries, color):
    pixels = image.load()
    for x, y in boundaries:
        pixels[x, y] = color
    return image


def run_funcs(old_image, new_image, path_for_new_images):
    print(old_image)
    image = read_image(old_image)
    print("Finished reading image")
    image = fix_image(image)
    print("Finished fixing image")
    boundaries = calc_boundaries(image)
    print("Finished calculating boundaries")
    image = mark_boundary(image, boundaries, (0, 0, 0))
    image = whiten(image)
    image = replace_white_and_black(image)
    orig_path = os.getcwd()
    os.chdir(path_for_new_images)
    save_image(new_image, image)
    os.chdir(orig_path)
    print("Finished for:")
    print(new_image)


def main():

    orig_path = os.getcwd() # change if images are in another path (inner folder or something)
    shapes_files = [f for f in listdir(orig_path) if isfile(join(orig_path, f)) and f.endswith('.bmp')]

    new_path = orig_path + '\\' + 'new_images'
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    for shape_file in shapes_files:
        shape_output = 'new_' + shape_file
        run_funcs(shape_file, shape_output, new_path)


if __name__ == "__main__":
    # main()
    deer_name = 'deer.bmp'
    im = read_image(deer_name)
    boundaries = calc_boundaries(im)
    im = mark_boundary(im, boundaries, (0, 0, 0))
    im = whiten(im)
    im = replace_white_and_black(im)
    im.save('new_' + deer_name)




