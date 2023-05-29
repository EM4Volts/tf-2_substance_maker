import os, sys
from wand import image
from PIL import Image, ImageEnhance
from PIL import ImageOps
titanfall_2_texture_set = [
    "ao.png",
    "col.png",
    "nml.png",
    "gls.png",
    "spc.png"    
]

texture_sets = [

]
texture_sets_filenames = [
     
]
tex_set = [
]


class bcolors:
     HEADER = '\033[95m'
     SPC = '\033[94m'
     GLS = '\033[92m'
     COL = '\033[93m'
     FAIL = '\033[91m'
     ENDC = '\033[0m'
     BOLD = '\033[1m'
     UNDERLINE = '\033[4m'


def generate_texture_sets(textures_in):
     for filename in os.scandir(textures_in):
            split_filename = filename.name.split("_")
            if not split_filename[0] in texture_sets:
               split_end_filename = "_".join(split_filename[:-1])
               tex_set.append(split_end_filename)
               texture_sets.append(split_filename[0])

def rename_textures(textures_in):
     for filename in os.scandir(textures_in):
          split_filename = filename.name.split("_")
          if split_filename[-1] == "AO.png":
               os.rename(textures_in + "/" + filename.name, textures_in + "/" + "".join(split_filename[:-1]) + "_ao.png")
          if split_filename[-1] == "Normal.png":
               os.rename(textures_in + "/" + filename.name, textures_in + "/" + "".join(split_filename[:-1]) + "_nml.png")
          if split_filename[-1] == "Specular.png":
               os.rename(textures_in + "/" + filename.name, textures_in + "/" + "".join(split_filename[:-1]) + "_tspc.png")
          if split_filename[-1] == "Diffuse.png":
               os.rename(textures_in + "/" + filename.name, textures_in + "/" + "".join(split_filename[:-1]) + "_col.png")
          if split_filename[-1] == "Metallic.png":
               os.rename(textures_in + "/" + filename.name, textures_in + "/" + "".join(split_filename[:-1]) + "_mtl.png")
          if split_filename[-1] == "Roughness.png":
               os.rename(textures_in + "/" + filename.name, textures_in + "/" + "".join(split_filename[:-1]) + "_rgh.png")
          if split_filename[-1] == "Glossiness.png":
               os.rename(textures_in + "/" + filename.name, textures_in + "/" + "".join(split_filename[:-1]) + "_tgls.png")

def make_source_specular(textures_path, texture_list):
     #check if _mtl.png and _col.png exist for each texture in texture_list
     #if they do, create a new texture called _spc.png
     for i in texture_list:
          if os.path.isfile(textures_path + "/" + i + "_mtl.png") and os.path.isfile(textures_path + "/" + i + "_col.png"):
               print(f"{bcolors.SPC}Creating specular map for {i}{bcolors.ENDC}")
               with Image.open(textures_path + "/" + i + "_mtl.png") as mtl:
                    with Image.open(textures_path + "/" + i + "_col.png") as col:
                         with Image.open(textures_path + "/" + i + "_tgls.png") as spc:
                              tgls = spc.convert("RGB")
                              mtl = mtl.convert("RGB")
                              col = col.convert("RGB")
                              mtl = ImageEnhance.Contrast(mtl).enhance(-0.15)
                              mtl = ImageEnhance.Brightness(mtl).enhance(0.15)
                              #multiply mtl and col together
                              mtl = Image.blend(mtl, col, 0.5)
                              #multiply mtl and spc together
                              mtl = Image.blend( tgls, mtl, 0.22)
                              mtl.save(textures_path + "/" + i + "_spc.png")

          
def make_source_gls(texture_path, texture_list):
     #check if _rgh.png then invert and save as _gls.png
     for i in texture_list:
          if os.path.isfile(texture_path + "/" + i + "_rgh.png"):
               print(f"{bcolors.GLS}Creating glossiness map for {i}{bcolors.ENDC}")
               with Image.open(texture_path + "/" + i + "_rgh.png") as rgh:
                    rgh = ImageOps.invert(rgh)
                    rgh.save(texture_path + "/" + i + "_gls.png")

def make_source_col(texture_path, texture_list):
     #check if _col.png and _tspc.png exist for each texture in texture_list
     #if they do, multiply them together and save as _col.png
     for i in texture_list:
          if os.path.isfile(texture_path + "/" + i + "_col.png") and os.path.isfile(texture_path + "/" + i + "_tspc.png"):
               print(f"{bcolors.COL}Creating color map for {i}{bcolors.ENDC}")
               with Image.open(texture_path + "/" + i + "_col.png") as col:
                    with Image.open(texture_path + "/" + i + "_tspc.png") as spc:
                         col = col.convert("RGB")
                         spc = spc.convert("RGB")
                         col = Image.blend(col, spc, 0.5)
                         col.save(texture_path + "/" + i + "_col.png")

def make_map(pakname, texname):
     temp_mat_string = str("")
     #open "base_pak.json" and load contents as string called "temp_json"
     #replace all instances of "PAKNAME" with pakname variable and save as "temp_json"
     with open("base_pak.json", "r") as f:
          temp_json = f.read()
          temp_json = temp_json.replace("PAKNAME", pakname)
          with open(pakname + "_map.json", "w") as f:
               f.write(temp_json)
     for i in texname:
          with open("material_include.json", "r") as f:
               temp_json = f.read()
               temp_json = temp_json.replace("TEXNAME", i)
               temp_json = temp_json.replace("PAKNAME", pakname)
               temp_mat_string += temp_json
     
     temp_mat_string = temp_mat_string[:-2]
              
     with open(pakname + "_map.json", "r") as f:
          contents = f.readlines()
     contents.insert(9, temp_mat_string)
     with open(pakname + "_map.json", "w") as f:
          contents = "".join(contents)
          f.write(contents)


def generate_repak_map(asset_path):
     pak_name = os.path.basename(asset_path)
     generate_texture_sets(asset_path)
     print(f"{bcolors.FAIL}Generating map for Texture Sets:{bcolors.ENDC}")
     for i in tex_set:
          print(f"{bcolors.GLS}{i}{bcolors.ENDC}")
     make_map(pak_name, tex_set)

def convert_textures(asset_path):
     for filename in os.scandir(asset_path):
          if filename.name.endswith("nml.png"):
               os.system("texconv.exe -f BC5_UNORM -srgb -ft dds " + filename.path + " -o " + asset_path)
          else:
               if filename.name.endswith("gls.png"):
                    os.system("texconv.exe -f BC4_UNORM -srgbi -ft dds " + filename.path + " -o " + asset_path)
               else:
                    os.system("texconv.exe -f BC1_UNORM_SRGB -srgbi -ft dds " + filename.path + " -o " + asset_path)

def move_textures(asset_path, tex_set):
     #delete contents of the folder "out_textures"
     for filename in os.scandir("out_textures"):
          os.remove(filename.path)

     #move each texture (ending specified in titanfall_2_texture_set list) to the folder "out_textures" for each texture set in tex_set
     for i in tex_set:
          for j in titanfall_2_texture_set:
               os.rename(asset_path + "/" + i + "_" + j, "out_textures/" + i + "_" + j)

def cleanup(asset_path):
     #delete all files in asset_path
     for filename in os.scandir(asset_path):
          os.remove(filename.path)

     #delete all .png files in "out_textures"
     for filename in os.scandir("out_textures"):
          if filename.name.endswith(".png"):
               os.remove(filename.path)

                              

if __name__ == "__main__":
     in_dir = sys.argv[1]
     #print the next statements in the color specified in bcolors as a header
     print(f"{bcolors.HEADER}Titanfall 2 Texture Workflow{bcolors.ENDC}")
     print(f"{bcolors.HEADER}Starting workflow{bcolors.ENDC}")
     print(f"{bcolors.HEADER}renaming textures{bcolors.ENDC}")
     rename_textures(in_dir)

     print(f"{bcolors.HEADER}generating texture list{bcolors.ENDC}")
     generate_texture_sets(in_dir)

     print(f"{bcolors.HEADER}generating specular maps{bcolors.ENDC}")
     make_source_specular(in_dir, tex_set)

     print(f"{bcolors.HEADER}generating glossiness maps{bcolors.ENDC}")
     make_source_gls(in_dir, tex_set)

     print(f"{bcolors.HEADER}generating color maps{bcolors.ENDC}")
     make_source_col(in_dir, tex_set)

     print(f"{bcolors.HEADER}moving textures{bcolors.ENDC}")
     move_textures(in_dir, tex_set)

     print(f"{bcolors.HEADER}converting textures{bcolors.ENDC}")
     convert_textures("out_textures/")

     print(f"{bcolors.HEADER}generating repak map{bcolors.ENDC}")
     generate_repak_map(in_dir)
     cleanup(in_dir)
     print(f"{bcolors.HEADER}workflow complete{bcolors.ENDC}")