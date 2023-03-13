from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Tornado Outbreak LCTX",".lctx")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    return 1   
def XGAddress2DTiledX(Offset, Width, TexelPitch):

    AlignedWidth = (Width + 31) & ~31

    LogBpp = (TexelPitch >> 2) + ((TexelPitch >> 1) >> (TexelPitch >> 2))
    OffsetB = Offset << LogBpp
    OffsetT = ((OffsetB & ~4095) >> 3) + ((OffsetB & 1792) >> 2) + (OffsetB & 63)
    OffsetM = OffsetT >> (7 + LogBpp)

    MacroX = ((OffsetM % (AlignedWidth >> 5)) << 2)
    Tile = ((((OffsetT >> (5 + LogBpp)) & 2) + (OffsetB >> 6)) & 3)
    Macro = (MacroX + Tile) << 3
    Micro = ((((OffsetT >> 1) & ~15) + (OffsetT & 15)) & ((TexelPitch << 3) - 1)) >> LogBpp

    return (Macro + Micro)


def XGAddress2DTiledY(Offset,Width,TexelPitch):
    AlignedWidth = (Width + 31) & ~31

    LogBpp = (TexelPitch >> 2) + ((TexelPitch >> 1) >> (TexelPitch >> 2))
    OffsetB = Offset << LogBpp
    OffsetT = ((OffsetB & ~4095) >> 3) + ((OffsetB & 1792) >> 2) + (OffsetB & 63)
    OffsetM = OffsetT >> (7 + LogBpp)

    MacroY = ((OffsetM // (AlignedWidth >> 5)) << 2)
    Tile = ((OffsetT >> (6 + LogBpp)) & 1) + (((OffsetB & 2048) >> 10))
    Macro = (MacroY + Tile) << 3
    Micro = ((((OffsetT & (((TexelPitch << 6) - 1) & ~31)) + ((OffsetT & 15) << 1)) >> (3 + LogBpp)) & ~1)

    return (Macro + Micro + ((OffsetT & 16) >> 4))
def XGUntileSurfaceToLinearTexture(data, width, height, textureTypeStr):

    destData = bytearray(len(data))
    blockSize = 0
    texelPitch = 0

    if textureTypeStr == "DXT1":
        blockSize = 4
        texelPitch = 8
    elif textureTypeStr == "DXT5":
        blockSize = 4
        texelPitch = 16
    elif textureTypeStr == "UNC":
        blockSize = 2;
        texelPitch = 4;
    elif textureTypeStr == "CTX1":
        blockSize = 4;
        texelPitch = 8;
    else:
        print("Bad dxt type!")
        return 0

    blockWidth = width // blockSize
    blockHeight = height // blockSize

    for j in range(blockHeight):
        for i in range(blockWidth):
            blockOffset = j * blockWidth + i

            x = XGAddress2DTiledX(blockOffset, blockWidth, texelPitch)
            y = XGAddress2DTiledY(blockOffset, blockWidth, texelPitch)

            srcOffset = j * blockWidth * texelPitch + i * texelPitch
            destOffset = y * blockWidth * texelPitch + x * texelPitch
            if destOffset < len(data):             
                destData[destOffset:destOffset+texelPitch] = data[srcOffset:srcOffset+texelPitch]

    return destData
def texType(bs,texName,texWidth,texHeight,texList,texType,texData):
    texName = texName
    if texType == 2:
        data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "A8R8G8B8")
        texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
    else:
        texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
def readLCTX(data,bs,texList):
    reader = NoeBitStream(data,NOE_BIGENDIAN)
    reader.seek(8)
    stringLength = reader.readUByte()
    texName = reader.readString()
    type = reader.readUInt()
    unk = reader.readUInt()
    print("Texture type is: " + str(type))
    mipMapCount = reader.readUByte()
    for i in range(mipMapCount):
        width = reader.readUInt()
        height = reader.readUInt()
        size = reader.readUInt()
        texData = reader.readBytes(size)
        if (type == 5):
            texData = rapi.swapEndianArray(texData,2)
            #texData = rapi.imageUntile360DXT(texData,width,height,8)
        if i == 0:
            texType(bs,texName,width,height,texList,type,texData)
def getTex(data,texList):
    bs = NoeBitStream(data,NOE_BIGENDIAN)
    bs.seek(0)
    check = bs.readUInt()
    if (check == 3):
        bs.seek(0x10)
        lctxDataSize = bs.readUInt()
        lctxData = bs.readBytes(lctxDataSize)
        readLCTX(lctxData,bs,texList)
    else:
        while (bs.tell() < os.path.getsize(rapi.getInputName())):
            lctxDataSize = bs.readUInt()
            lctxData = bs.readBytes(lctxDataSize)
            readLCTX(lctxData,bs,texList)
    return 1
    