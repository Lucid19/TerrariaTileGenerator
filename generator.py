from PIL import Image, ImageDraw
import numpy as np
import matplotlib.colors as colors

# Highest order function that generates the tile
def generate_tile(color, shades, consistency, name):
    # generating possibile shades
    shades = generate_shades(shades, consistency, color)
    # generating the matrix of colors
    block = generate_matrix(np.array([]), shades, consistency)
    # synthesising image
    generate_block(block, name, shades)

# Generating Shades for Tile
def generate_shades(shades, consistency, color):
    # turning into HSV format
    (h, s, v) = colors.rgb_to_hsv(colors.to_rgb(color))
    color = (h, s, v)

    # Ratios
    hr= (consistency*(1/360))*340+0.05
    sr= consistency*0.8+0.2
    vr= consistency*0.8+0.2

    # determining the minimum value
    hmin = h-hr/2
    smin = s-sr/2
    vmin = v-vr/2

    # creating shades
    shade_list = np.array([])
    for shade in range(shades-1):
        multiplier=np.random.uniform(0,1)

        # initial values
        h = hmin + multiplier*hr
        s = smin + multiplier*hr
        v = vmin + multiplier*hr

        while( 1 < s  or s < 0 or 1 < v  or v < 0 or 1 < h or h < 0):
            multiplier=np.random.uniform(0,1)

            # new values
            h = hmin + multiplier*hr
            s = smin + multiplier*hr
            v = vmin + multiplier*hr
        # when done 
        shade_list = np.concatenate((shade_list, (h, s, v)), axis=0)
    shade_list = np.concatenate((shade_list, (color)), axis=0)
    shade_list = shade_list.reshape(shades, 3)
    return shade_list

def generate_block(block, name):
    image = Image.open("TTG.png")
    for j in range(15*18):
        for i in range(16*18):
            if i % 2 == 0 and j % 2 == 0:
                current_pixel=image.getpixel((i, j))
                if current_pixel == (0, 255, 0, 255):
                    if j != 0 and i != 0:
                        (r, g, b) = colors.hsv_to_rgb(block[int(j/2)][int(i/2)])
                    elif j!= 0 and i==0:
                        (r, g, b) = colors.hsv_to_rgb(block[int(j/2)][i])
                    elif j==0 and i!=0:
                        (r, g, b) = colors.hsv_to_rgb(block[j][int(i/2)])
                    else:
                        (r, g, b) = colors.hsv_to_rgb(block[j][i])
                    image.putpixel((i,j), (round(r*255), round(g*255), round(b*255)))
                    image.putpixel((i+1,j+1), (round(r*255), round(g*255), round(b*255)))
                    image.putpixel((i,j+1), (round(r*255), round(g*255), round(b*255)))
                    image.putpixel((i+1,j), (round(r*255), round(g*255), round(b*255)))
#                elif current_pixel == (30, 0, 25, 255):
#                    (r, g, b) = colors.hsv_to_rgb(shades[len(shades)-1])
#                    image.putpixel((i,j), (round(r*255), round(g*255), round(b*255)))
#                    image.putpixel((i+1,j+1), (round(r*255), round(g*255), round(b*255)))
#                    image.putpixel((i,j+1), (round(r*255), round(g*255), round(b*255)))
#                    image.putpixel((i+1,j), (round(r*255), round(g*255), round(b*255)))
    image.save(name+".png")

def calculate_shade(previous_shades, consistency, shades):
    for previous_shade in previous_shades:
        probability = (1/(len(shades)-1))*(consistency+1)
        shade_chosen = np.random.uniform(0, 1)
        if shade_chosen < probability:
            return previous_shade
    return shades[np.random.randint(0, len(shades)-2)]

def generate_matrix(block, shades, consistency):
    for j in range(9*15):
        for i in range(16*9):
            if j==0:
                if i==0:
                    shade = shades[np.random.randint(0, len(shades)-2)]
                else:
                    block = block.reshape((j*16*9+i), 3)
                    previous_shades = np.array([block[i-1]])
                    shade = calculate_shade(previous_shades, consistency, shades)
            elif i==0:
                block = block.reshape((j*16*9+i), 3)
                previous_shades = np.array([block[(j-1)*15*9], block[(j-1)*15*9+1]])
                shade = calculate_shade(previous_shades, consistency, shades)
            elif i==16*9-1:
                block = block.reshape((j*16*9+i), 3)
                previous_shades = np.array([block[j*15*9-1], block[j*15*9-2], block[(j-1)*15*9-2]])
                shade = calculate_shade(previous_shades, consistency, shades)
            else:
                block = block.reshape((j*16*9+i), 3)
                previous_shades = np.array([block[j*15*9+i-1], block[(j-1)*15*9+i-2], block[(j-1)*15*9+i], block[(j-1)*15*9+i-1]])
                shade = calculate_shade(previous_shades, consistency, shades)
            vector = np.array(shade)
            block = block.reshape((j*16*9+i)*3)
            block= np.concatenate((block, vector), axis=0)
    return block.reshape(9*15, 16*9, 3)