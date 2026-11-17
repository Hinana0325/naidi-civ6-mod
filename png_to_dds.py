"""PNG(8bit, RGBA/RGB) -> 未压缩 32bpp DDS（带 alpha），无需 PIL。
用法: python png_to_dds.py <in.png> <out.dds>
"""
import struct, sys, zlib, os


def read_png(path):
    data = open(path, "rb").read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG: " + path)
    pos = 8
    width = height = bitdepth = colortype = interlace = None
    idat = b""
    while pos < len(data):
        length = struct.unpack_from(">I", data, pos)[0]
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bitdepth, colortype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
    if bitdepth != 8 or interlace != 0:
        raise ValueError(f"只支持 8bit 非隔行 PNG，实际 bit={bitdepth} interlace={interlace}")
    if colortype not in (2, 6):
        raise ValueError(f"只支持 RGB(2)/RGBA(6)，实际 colortype={colortype}")
    nch = 4 if colortype == 6 else 3
    raw = zlib.decompress(idat)
    stride = width * nch
    out = bytearray(height * stride)
    prev = bytearray(stride)

    def paeth(a, b, c):
        p = a + b - c
        pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
        if pa <= pb and pa <= pc:
            return a
        return b if pb <= pc else c

    p = 0
    for y in range(height):
        ft = raw[p]; p += 1
        line = bytearray(raw[p:p + stride]); p += stride
        if ft == 1:
            for i in range(nch, stride):
                line[i] = (line[i] + line[i - nch]) & 0xFF
        elif ft == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ft == 3:
            for i in range(stride):
                left = line[i - nch] if i >= nch else 0
                line[i] = (line[i] + ((left + prev[i]) >> 1)) & 0xFF
        elif ft == 4:
            for i in range(stride):
                left = line[i - nch] if i >= nch else 0
                upleft = prev[i - nch] if i >= nch else 0
                line[i] = (line[i] + paeth(left, prev[i], upleft)) & 0xFF
        elif ft != 0:
            raise ValueError("未知 PNG 过滤器: " + str(ft))
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return width, height, nch, out


def write_dds(path, w, h, pixels):
    header = bytearray()
    header += struct.pack("<I", 124)
    header += struct.pack("<I", 0x1 | 0x2 | 0x4 | 0x8 | 0x1000)
    header += struct.pack("<I", h)
    header += struct.pack("<I", w)
    header += struct.pack("<I", w * 4)
    header += struct.pack("<I", 0)
    header += struct.pack("<I", 0)
    header += b"\x00" * (4 * 11)
    header += struct.pack("<I", 32)
    header += struct.pack("<I", 0x1 | 0x40)
    header += struct.pack("<I", 0)
    header += struct.pack("<I", 32)
    header += struct.pack("<I", 0x00ff0000)
    header += struct.pack("<I", 0x0000ff00)
    header += struct.pack("<I", 0x000000ff)
    header += struct.pack("<I", 0xff000000)
    header += struct.pack("<I", 0x1000)
    header += struct.pack("<I", 0) * 3
    header += struct.pack("<I", 0)
    with open(path, "wb") as f:
        f.write(b"DDS ")
        f.write(bytes(header))
        f.write(pixels)


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    w, h, nch, px = read_png(src)
    # PNG 解出来已是 RGBA 顺序；游戏按 byte0=R 读，故直接写入，不再交换
    out = bytearray(len(px) // nch * 4)
    if nch == 4:
        out[:] = px
    else:
        out[0::4] = px[0::3]
        out[1::4] = px[1::3]
        out[2::4] = px[2::3]
        out[3::4] = b"\xff" * (len(px) // 3)
    write_dds(dst, w, h, bytes(out))
    print(f"{os.path.basename(dst)}  {w}x{h}  {os.path.getsize(dst)//1024} KB")
