
from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Phoenix Wright Ace Attorney OBM",".obm")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    return 1   

def getTex(data,texList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0x03)
    paletteSize = bs.readUByte() #??? idk 
    texWidth = bs.readUShort()
    texHeight = bs.readUShort()
    print(texWidth,texHeight)
    texName = os.path.splitext(rapi.getInputName())[0]
    if paletteSize == 8:
        palData = bs.readBytes(512)
        texData = bs.readBytes(texWidth*texHeight)
    elif paletteSize == 4:
        palData = bs.readBytes(32)
        texData = bs.readBytes(texWidth*texHeight//2)
        texData = noesis.nybbleSwap(texData) 
    if paletteSize == 8:
        Data = rapi.imageDecodeRawPal(texData,palData,texWidth,texHeight,8,"a1b5g5r5")
    elif paletteSize == 4:
        Data = rapi.imageDecodeRawPal(texData,palData,texWidth,texHeight,4,"a1b5g5r5")
    texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
    return 1