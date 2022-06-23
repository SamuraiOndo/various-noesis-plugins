
from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Wall-e Bitmap_Z",".Bitmap_Z")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    return 1   

def getTex(data,texList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(4)
    linksize = bs.readUInt()
    texSize = bs.readUInt()
    bs.seek(0x25)
    for i in range(1):
        texWidth = bs.readUInt()
        texHeight = bs.readUInt()
        texFmt = bs.readUInt()
        ignore1 = bs.readUInt()
        ignore3 = bs.readUInt()
        texType(bs,data,texSize,texWidth,texHeight,texList)
        print(texWidth, texHeight)
    print(texWidth, texHeight)
    return 1
    
def texType(bs,texSize,texName,texWidth,texHeight,texList):
    bs.seek(0x2d)
    ddscheck = bs.readUInt()
    print(ddscheck)
    if ddscheck != 0:
        ddssize = (ddscheck - 0x80)
        bs.seek(0x8a)
        ddstype = bs.readString()
        print(ddstype)
        bs.seek(0xb6)
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        texData = bs.readBytes(ddssize)
        if ddstype == "DXT1":
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
        if ddstype == "DXT5":
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
    if ddscheck == 0:
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        bs.seek(0x36)
        texData = bs.readBytes(texWidth * texHeight * 2)
        data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R8G8")
        texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))