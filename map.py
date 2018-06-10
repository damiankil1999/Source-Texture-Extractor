"""
Main file for map parsing.
@author damiankil1999
"""
import os
import sys
import time
import parse
import shutil
import tkinter
import tkinter.filedialog
from colorama import init, Fore, Back

init(convert=True)
tkinter.Tk().withdraw()
mdlext = {".dx80.vtx", ".dx90.vtx", ".phy", ".sw.vtx", ".vvd"}

# Location of the models and materials folder
gamefolder = tkinter.filedialog.askdirectory(title="Location of the models and materials folder. E.g GarrysMod/garrysmod", mustexist=True)
print(Fore.MAGENTA + "Content folder: " + Fore.GREEN + gamefolder + Fore.WHITE)
if not os.path.isdir(gamefolder):
    print(Fore.RED + "Error: Game folder is invalid!" + Fore.WHITE)
    sys.exit()

extract = tkinter.filedialog.askdirectory(title="Extraction folder", mustexist=True)
print(Fore.MAGENTA + "Extraction folder: " + Fore.GREEN + extract + Fore.WHITE)
if not os.path.isdir(extract):
    print(Fore.RED + "Error: Extraction folder is invalid!" + Fore.WHITE)
    sys.exit()

mapfile = tkinter.filedialog.askopenfilename(title="Select the map file", initialdir=gamefolder+"/maps", filetypes=(("Valve Map Format", "*.vmf"),))
print(Fore.MAGENTA + "Map file: " + Fore.GREEN + mapfile + Fore.WHITE)
if not mapfile.endswith(".vmf"):
    print(Fore.RED + "Error: map is invalid!" + Fore.WHITE)
    sys.exit()

time.sleep(1) # Give the user a second to check if everything is correct.
STARTTIME = time.time()

print(Fore.MAGENTA + "\nReading map file... ", end="")
VMFTimer = time.time()
materials, models = parse.VMF(mapfile)
print(Fore.GREEN + "Done! took " + Fore.CYAN + str(round(time.time() - VMFTimer, 4)) + Fore.GREEN + " seconds." + Fore.WHITE)
print(Fore.BLUE + "Found " + Fore.GREEN + str(len(materials)) + Fore.BLUE + " unique materials and " + Fore.GREEN + str(len(models)) + Fore.BLUE + " unique models in the map.\n")

handledfiles = []
failed = 0

def HandleFile(f):
    global mdlext, handledfiles, failed

    if f in handledfiles:
        return
    handledfiles.append(f)

    print(Fore.BLUE + f)
    print(Fore.MAGENTA + "\tFile exists? ", end="")
    if os.path.isfile(f):
        print(Fore.GREEN + "Yes.")

        # Copy file...
        start = time.time()
        print(Fore.MAGENTA + "\tCopying file... ", end="")
        try:
            path = "/".join(f.replace(gamefolder, extract).split("/")[:-1])
            os.makedirs(path, exist_ok=True)
            shutil.copy(f, path)
            print(Fore.GREEN + "Done! took " + Fore.CYAN + str(round(time.time() - start, 4)) + Fore.GREEN + " seconds.")
        except:
            print(Fore.RED + "Failed!")
            return
        else:
            if f.endswith(".mdl"):
                for ext in mdlext:
                    HandleFile(f.replace(".mdl", ext))
            elif f.endswith(".vmt"):
                start = time.time()
                print(Fore.MAGENTA + "\tParsing VMT file... ", end="")
                vmts, vtfs = parse.VMT(f)
                print(Fore.GREEN + "Done! took " + Fore.CYAN + str(round(time.time() - start, 4)) + Fore.GREEN + " seconds.")
                for fi in vtfs + vmts: # Preformance vs beauty
                    print(Fore.LIGHTBLACK_EX + "\t\t" + fi[0] + "\t" + fi[1])
                for vtf in vtfs:
                    HandleFile(gamefolder + "/materials/" + vtf[1].replace("\"", "").replace("\'", "") + ".vtf")
                for vmt in vmts:
                    HandleFile(gamefolder + "/" + vmt[1].replace("\"", "").replace("\'", ""))
    else:
        print(Fore.RED + "No.")
        failed = failed + 1

# Materials.
for material in materials:
    HandleFile(gamefolder + "/materials/" + material + ".vmt")

for model in models:
    HandleFile(gamefolder + "/" + model)

print(Fore.GREEN + "Completed! Total time taken: " + Fore.CYAN + str(round(time.time() - STARTTIME, 4)) + Fore.GREEN + " seconds.")
if failed > 0:
    print(Fore.CYAN + str(failed) + Fore.RED + " files could not be found inside the specified content folder.")

input("Press enter to close.")
