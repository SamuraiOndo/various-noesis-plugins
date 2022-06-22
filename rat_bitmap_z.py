# Edness   2021-07-15


from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Ratatouille Bitmap_Z",".Bitmap_Z")
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
    bs.seek(0x18)
    bs.seek(linksize,1)
    for i in range(1):
        texWidth = bs.readUInt()
        texHeight = bs.readUInt()
        texFmt = bs.readUInt()
        ignore1 = bs.readUInt()
        ignore3 = bs.readUInt()
        texType(bs,data,texSize,texWidth,texHeight,texList)
        print(texWidth, texHeight)
    return 1
    
def texType(bs,texSize,texName,texWidth,texHeight,texList):
    bs.seek(0x28)
    ddscheck = bs.readUInt()
    if ddscheck != 0:
        ddssize = (ddscheck - 0x80)
        bs.seek(0x88)
        ddstype = bs.readString()
        print(ddstype)
        bs.seek(0xb4)
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        texData = bs.readBytes(ddssize)
        if ddstype == "DXT1":
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
        if ddstype == "DXT5":
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
    if ddscheck == 0:
        bs.seek(0x2c)
        versionnum = bs.readBytes(0x01)
        print(versionnum)
        if versionnum == b'\x0c':
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            bs.seek(0x34)
            texData = bs.readBytes(texWidth * texHeight * 4)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8A8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        if versionnum == b'\x0d':
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            bs.seek(0x34)
            texData = bs.readBytes(texWidth * texHeight * 3)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))