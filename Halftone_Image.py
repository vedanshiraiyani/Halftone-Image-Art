from PIL import Image, ImageDraw
import math



# Determining the vertices of stars based on the centre and star size along with the sharpness of star (size in the below code is used to determing the ratio of distance of centre to outer point and distance of centre to inner point)
def vertices_star(center_x, center_y, size, star_size):
    vertices_star = []

    for i in range(12):
        angle_deg = 360 / 12 * i
        angle_rad = math.pi / 180 * angle_deg
        if i % 2 == 0:
            x = center_x + star_size * math.cos(angle_rad)
            y = center_y + star_size * math.sin(angle_rad)
        else:
            x = center_x + star_size / size * math.cos(angle_rad)
            y = center_y + star_size / size * math.sin(angle_rad)
        vertices_star.append((x, y))
    return vertices_star



# Determing the vertices of hexagon based and given centre of hexagon
def vertices(x, y):
    vertices_hex = []
    num_sides = 6
    poly_size = 20

    for i in range(num_sides):
        angle_deg = 360 / num_sides * i
        angle_rad = math.pi / 180 * angle_deg
        a = x + poly_size * math.cos(angle_rad)
        b = y + poly_size * math.sin(angle_rad)
        vertices_hex.append((a, b))
    return vertices_hex




# opening the image
input_image = Image.open(r"C:\Users\hp\Desktop\input_image.JPG").convert("L")
new_image = input_image.resize((input_image.size[0]*10, input_image.size[1]*10)) # resizing should be done based on the size of input image
# print(new_image.size)

# determing the thresholds of brightness and star sizes(used to map with stars and hexagons)
thresholds = [0, 30, 45, 70, 90, 120, 145, 160, 190, 220, 251]
output_image = Image.new("L", new_image.size, "black")
draw = ImageDraw.Draw(output_image)
size = [4.7, 4.4, 4.1, 3.8, 3.5, 3.2, 2.9, 2.6, 2.3, 2.0]
star_size = 21
polygon_count = 0
dot_size = 40


# iterating through the canvas with steps of fixed number of pixels as step size and drawing stars or hexagons

for x in range(0, new_image.width, dot_size):
    for y in range(0, new_image.height, dot_size):
        brightness = 0
        count = 0
        for i in range(dot_size):
            for j in range(dot_size):
                if x+i < new_image.width and y+j < new_image.height:
                    pixel = new_image.getpixel((x+i, y+j))
                    brightness += pixel
                    count += 1
        brightness //= count

        for i in range(len(thresholds)):
            if brightness >= thresholds[i] and i==(len(thresholds)-1):
                points = vertices(x, y)
                draw.polygon(points, fill="white", outline="black")
                polygon_count += 1
            elif brightness >= thresholds[i]:
                points = vertices_star(x, y, size[i], star_size)
                draw.polygon(points, fill="white", outline = "black")
                polygon_count += 1



output_image.save("output_image.jpg")
print(polygon_count) #printing the total polygon count in the entire image
