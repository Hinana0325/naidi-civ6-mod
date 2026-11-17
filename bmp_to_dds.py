"""把 32 位 BMP 转成未压缩 32bpp DDS（无需 PIL）。
用法: python bmp_to_dds.py <in.bmp> <out.dds>
"""
import struct, sys, os

def read_bmp(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"BM":
        raise ValueError("not a BMP: " + path)
    off = struct.unpack_from("<I", data, 10)[0]
    hdr = struct.unpack_from("<I", data, 14)[0]
    w, h = struct.unpack_from("<ii", data, 18)
    bpp = struct.unpack_from("<H", data, 28)[0]
    comp = struct.unpack_from("<I", data, 30)[0]
    if bpp != 32 or comp != 0:
        raise ValueError(f"需要 32bpp 未压缩 BMP，实际 {bpp}bpp comp={comp}")
    top_down = h < 0
    h = abs(h)
    stride = w * 4
    rows = []
    pos = off
    for _ in range(h):
        rows.append(data[pos:pos + stride])
        pos += stride
    if not top_down:
        rows.reverse()
    return w, h, b"".join(rows)

def write_dds(path, w, h, pixels):
    header = bytearray()
    header += struct.pack("<I", 124)                 # dwSize
    header += struct.pack("<I", 0x1 | 0x2 | 0x4 | 0x8 | 0x1000)  # caps|height|width|pitch|pixelformat
    header += struct.pack("<I", h)
    header += struct.pack("<I", w)
    header += struct.pack("<I", w * 4)               # pitch
    header += struct.pack("<I", 0)                   # depth
    header += struct.pack("<I", 0)                   # mipmaps
    header += b"\x00" * (4 * 11)                     # reserved
    header += struct.pack("<I", 32)                  # pf size
    header += struct.pack("<I", 0x1 | 0x40)          # alphapixels|rgb
    header += struct.pack("<I", 0)                   # fourcc
    header += struct.pack("<I", 32)                  # rgbbits
    header += struct.pack("<I", 0x00ff0000)          # R
    header += struct.pack("<I", 0x0000ff00)          # G
    header += struct.pack("<I", 0x000000ff)          # B
    header += struct.pack("<I", 0xff000000)          # A
    caps = bytearray()
    caps += struct.pack("<I", 0x1000)                # texture
    caps += struct.pack("<I", 0) * 3
    caps += struct.pack("<I", 0)                     # reserved2
    header += caps
    with open(path, "wb") as f:
        f.write(b"DDS ")
        f.write(bytes(header))
        f.write(pixels)

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    w, h, px = read_bmp(src)
    # BMP 的 32bpp 像素是 BGRA 排列；实测游戏渲染时按 RGBA 解读，
    # 所以这里交换 R/B，写出后画面才是正确色相。
    swapped = bytearray(len(px))
    swapped[0::4] = px[2::4]
    swapped[1::4] = px[1::4]
    swapped[2::4] = px[0::4]
    swapped[3::4] = px[3::4]
    write_dds(dst, w, h, bytes(swapped))
    print(f"{os.path.basename(dst)}  {w}x{h}  {os.path.getsize(dst)//1024} KB")
