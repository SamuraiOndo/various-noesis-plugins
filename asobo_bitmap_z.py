
from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Bitmap_Z",".Bitmap_Z")
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
    bs.seek(0x04)
    version = bs.readUInt()
    print(version)
    if version == 13:
        for i in range(1):
            bs.seek(0x25)
            texWidth = bs.readUInt()
            texHeight = bs.readUInt()
            texFmt = bs.readUInt()
            ignore1 = bs.readUInt()
            ignore3 = bs.readUInt()
            texType(bs,data,texSize,texWidth,texHeight,texList)
            print(texWidth, texHeight)
    if version == 8:
        for i in range(1):
            bs.seek(0x20)
            texWidth = bs.readUInt()
            texHeight = bs.readUInt()
            texFmt = bs.readUInt()
            ignore1 = bs.readUInt()
            ignore3 = bs.readUInt()
            texType(bs,data,texSize,texWidth,texHeight,texList)
            print(texWidth, texHeight)
    if version == 1056:
        for i in range(1):
            bs.seek(0x1e)
            texWidth = bs.readUInt()
            texHeight = bs.readUInt()
            texFmt = bs.readUInt()
            ignore1 = bs.readUInt()
            ignore3 = bs.readUInt()
            texType(bs,data,texSize,texWidth,texHeight,texList)
            print(texWidth, texHeight)
    if version == 96:
        for i in range(1):
            bs.seek(0x1e)
            texWidth = bs.readUInt()
            texHeight = bs.readUInt()
            texFmt = bs.readUInt()
            ignore1 = bs.readUInt()
            ignore3 = bs.readUInt()
            texType(bs,data,texSize,texWidth,texHeight,texList)
            print(texWidth, texHeight)
    if version == 32:
        for i in range(1):
            bs.seek(0x1e)
            texWidth = bs.readUInt()
            texHeight = bs.readUInt()
            texFmt = bs.readUInt()
            ignore1 = bs.readUInt()
            ignore3 = bs.readUInt()
            texType(bs,data,texSize,texWidth,texHeight,texList)
            print(texWidth, texHeight)
    bs.seek(0x8)
    version = bs.readUInt()
    if version == 2667163991:
        for i in range(1):
            bs.seek(0x14)
            texWidth = bs.readUInt()
            texHeight = bs.readUInt()
            texFmt = bs.readUInt()
            ignore1 = bs.readUInt()
            ignore3 = bs.readUInt()
            texType(bs,data,texSize,texWidth,texHeight,texList)
            print(texWidth, texHeight)
        
    return 1
    
def texType(bs,texSize,texName,texWidth,texHeight,texList):
    bs.seek(0x4)
    version = bs.readUInt()
    if version == 13:
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
    if version == 8:
        bs.seek(0x28)
        ddscheckrat = bs.readUInt()
        if ddscheckrat != 0:
            ddssize = (ddscheckrat - 0x80)
            bs.seek(0x88)
            ddstyperat = bs.readString()
            print(ddstyperat)
            bs.seek(0xb4)
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(ddssize)
            if ddstyperat == "DXT1":
                texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
            if ddstyperat == "DXT5":
                texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
        if ddscheckrat == 0:
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
            if versionnum == b'\x07':
                texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
                bs.seek(0x34)
                texData = bs.readBytes(texWidth * texHeight)
                data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R2G2B2A2")
                texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
    if version == 1056:
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        bs.seek(0x38)
        palData = bs.readBytes(0x400)
        texData = bs.readBytes(texWidth*texHeight)
        untwiddle = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 8)
        Data = rapi.imageDecodeRawPal(untwiddle,palData,texWidth,texHeight,8,"R8G8B8A8",noesis.DECODEFLAG_PS2SHIFT)
        texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
    if version == 96:
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        bs.seek(0x38)
        palData = bs.readBytes(0x40)
        texData = bs.readBytes(texWidth*(texHeight//2))
        untwiddle = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 4)
        Data = rapi.imageDecodeRawPal(untwiddle,palData,texWidth,texHeight,4,"R8G8B8A8")
        texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
    if version == 96:
        texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
        bs.seek(0x38)
        texData = bs.readBytes(texWidth*texHeight*2)
        untwiddle = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 4)
        Data = rapi.imageDecodeRaw(texData,texWidth,texHeight,"R16G16B16A16")
        texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
    bs.seek(0x8)
    version = bs.readUInt()
    if version == 2667163991:
        bs.seek(0x1c)
        ddscheckrat = bs.readUInt()
        if ddscheckrat != 0:    
            ddssize = (ddscheckrat - 0x80)
            bs.seek(0xA8)
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(ddssize)
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
        else:
            bs.seek(0x20)
            versionnum = bs.readBytes(0x01)
            if versionnum == b'\x0d':
                bs.seek(0x28)
                texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
                texData = bs.readBytes(texWidth * texHeight * 3)
                data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R8G8B8")
                texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
            if versionnum == b'\x0c':
                bs.seek(0x28)
                texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
                texData = bs.readBytes(texWidth * texHeight * 4)
                data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8g8b8a8")
                texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        