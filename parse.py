"""
File parser.

@author damiankil1999

Just Reference table - Files:
    - VTF: Valve Texture Format, The actual picture
    - VMT: Valve Material Type, The $keyvalues file for the texture.
    - VMF: Valve Map format, The decompiled map.
    - SMD: Studiomdl Data, A decompiled model.
    - DMX: A newer version of the SMD format.
    - QC: A KeyValues file.
"""

def KV(line):
    """
    Key Values line parser.
    Return values still have the quotation marks for additional parsing.
    @return str key, str value
    """
    nl = line.replace("\t", " ").replace("\\", "/").strip().split(" ")
    return nl[0], "".join(nl[1:]).strip()


def QC(file):
    """
    Parses a Key Values file for models.
    @return list keyvalues(str key, str value)
    """
    raise NotImplementedError()


def VMT(file):
    """
    Parses the VMT file
    @return list vmts, list vtfs
    """
    vmts = []
    vtfs = []

    # 0 = VMT, 1 = VTF, 2 = both
    klist = {
        "ambientoccltexture": 1,
        "basetexture": 1,
        "basetexture2": 1,
        "basetexture3": 1,
        "basetexture4": 1,
        "blendmodulatetexture": 1,
        "bottommaterial": 1,
        "bumpmap": 1,
        "bumpmap2": 1,
        "detail": 1,
        "envmap": 1,
        "envmapmask": 1,
        "fleshbordertexture1d": 1,
        "fleshcubetexture": 1,
        "fleshinteriornoisetexture": 1,
        "fleshinteriortexture": 1,
        "fleshnormaltexture": 1,
        "fleshsubsurfacetexture": 1,
        "normalmap": 1,
        "parallaxmap": 1,
        "phongexponenttexture": 1,
        "ramptexture": 1,
        "underwateroverlay": 1,
        "%tooltexture": 1,
        "include": 0,
    }
    try:
        with open(file) as f:
            for line in f:
                key, value = KV(line)
                key = key.replace("\"", "").replace("\'", "").replace("$", "").lower()
                for k, v in klist.items():
                    if k == key:
                        if v >= 1:
                            vtfs.append((k, value))
                        if v == 0 or v == 2:
                            vmts.append((k, value))
                        break
    except:
        pass
    return vmts, vtfs


def VMF(file):
    """
    Parse a map file.
    @returns list materials, list models
    """
    materials = []
    models = []
    try:
        with open(file) as f:
            for line in f:
                if "\"material\"" in line:
                    value = KV(line)[1].replace("\"", "").replace("\'", "")
                    if value not in materials:
                        materials.append(value)
                elif "\"model\"" in line:
                    value = KV(line)[1].replace("\"", "").replace("\'", "")
                    if value not in models:
                        models.append(value)
    except:
        pass
    return materials, models
