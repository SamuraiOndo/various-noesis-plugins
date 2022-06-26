from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Anohana PSP",".PSP")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    return 1   

def getTex(data,texList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    texSize = 1
    bs.seek(0x02)
    for i in range(1):
        texWidth = bs.readUShort()
        texHeight = bs.readUShort()
        texType(bs,data,texSize,texWidth,texHeight,texList)
        print(texWidth, texHeight)
    return 1
    
def texType(bs,texSize,texName,texWidth,texHeight,texList):
    bs.seek(0x0)
    versionnumber = bs.readUShort()
    print(versionnumber)
    if versionnumber == 3:
        bs.seek(0x10)
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        texData = bs.readBytes(texWidth * texHeight * 2)
        untwiddle = rapi.imageUntwiddlePSP(texData, texWidth, texHeight, 16)
        data = rapi.imageDecodeRaw(untwiddle, texWidth, texHeight,"R4G4B4A4")
        texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
    if versionnumber == 9:
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        bs.seek(0x10)
        palData = bs.readBytes(0x200)
        bs.seek(0x210)
        texData = bs.readBytes(texWidth*texHeight)
        untwiddle = rapi.imageUntwiddlePSP(texData, texWidth, texHeight, 8)
        Data = rapi.imageDecodeRawPal(untwiddle,palData,texWidth,texHeight,8,"r5g5b5p1")
        texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
    if versionnumber == 11:
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        bs.seek(0x10)
        palData = bs.readBytes(0x400)
        bs.seek(0x410)
        texData = bs.readBytes(texWidth*texHeight)
        untwiddle = rapi.imageUntwiddlePSP(texData, texWidth, texHeight, 8)
        Data = rapi.imageDecodeRawPal(untwiddle,palData,texWidth,texHeight,8,"R8G8B8A8")
        texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))