
# # tf-2_substance_maker
Converts VERY SPECIFIC substance painter texture outputs to a sort of good looking titanfall 2 material
auto generates a repak map that uses a color, normal, gloss, spec and AO texture






## Setup


Download the latest release zip and unzip somewhere on your PC (only tested on windows)

Make sure you have Python 3.10+ installed

In Substance Painter make sure you have the following things setup:

# For your Texture sets make sure the following channels exist 

(might work properly without them but sometimes substance painter didnt export some maps for some reason)

![1](https://media.discordapp.net/attachments/310443386429767690/1112555378308288544/image.png?width=639&height=427)


# Make an Export template like this: 

![2](https://media.discordapp.net/attachments/310443386429767690/1112555223559442523/image.png?width=950&height=670)

(if you dont know how, the colored rectangles corespond to the ones on the maps on the right)

THE NAMING MATTERS DO NOT RENAME THE MAP NAMES AT ALL, NAME THEM LIKE IN THE SCREENSHOT

# Make sure to bake your mesh maps

edit > bake mesh maps

make sure to select the mesh file like in the screnshot bellow

![3](https://media.discordapp.net/attachments/310443386429767690/1112554754380398644/image.png?width=877&height=625)

# Before exporting make sure that in the general export parameters 8 Bit PNG is selected and that your texture set names do not contain any "_", "-", other special characters or spaces (example bellow)

![4](https://media.discordapp.net/attachments/310443386429767690/1112555261253648464/image.png?width=660&height=292)

![5](https://media.discordapp.net/attachments/310443386429767690/1112558229600354415/image.png?width=653&height=231)

otherwise the script will fail cuz 16 bit bad
if your exported diffuse maps dont have the color you expect make sure to set the "base color" and "diffuse" channels the same color (substance painter may not export diffuse correctly if both arent same)


# The unzipped folder should look like this:

![6](https://media.discordapp.net/attachments/310443386429767690/1112557511216742411/image.png?width=557&height=136)
DO NOT TOUCH ANY OF THE FILES

## Done! ur fully setup. Usage bellow.



# USAGE

1. make a folder in this folder and name it the way your pak is supposed to be called (in the example its called "cool_pak_name"):

![7](https://media.discordapp.net/attachments/310443386429767690/1112559153567776808/image.png?width=554&height=131)

2. put your unedited, not self renamed exported Substance Painter textures in that new folder, dont move them, copy them, the folder gets cleared after a conversion
3. open a terminal/cmd in side the same folder the script (main.py) is in
4. in the terminal type ```py(or whatever youve setup to call python 3.10+ from cmd) main.py cool_pak_name```
where you replace "cool_pak_name" with your folder name

5. Press enter and it should start making your textures and the map. 
Your textures will be in the "out_textures" folder once done, the repak map will put the textures in the path ```texture/models/weapons_r2/cool_pak_name/``` once again "cool_pak_name" is your folder name, so make sure to put the textures into that folder in your repak assets folder.

### Thats about it, i think. Works for me, dont judge my shitty code lul, doesnt work for you or you have problems? Message me on discord. "4V with the 4 as a picture"


## License

[GPL3](https://github.com/EM4Volts/tf-2_substance_maker/blob/main/LICENSE)

Textconv.exe from Microsofts DirectXTex tools [DIREXTXTEX](https://github.com/microsoft/DirectXTex)
