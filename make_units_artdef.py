"""从游戏基础 Units.artdef 里复制 UNIT_SCOUT / UNIT_WARRIOR / UNIT_BUILDER 三个完整条目，
改名为奶家三兵种，生成 mod 的 Units.artdef（模板 Units，与基础文件合并）。"""
import xml.etree.ElementTree as ET

SRC = r"C:\Program Files (x86)\Steam\steamapps\common\Sid Meier's Civilization VI\Base\ArtDefs\Units.artdef"
DST = r"C:\Users\jq200\Doubao\chats\2026-11-13\new-chat-1\NaiwaCiv\ArtDefs\Units.artdef"

RENAME = {
    "UNIT_SCOUT": "UNIT_NAIWA_DOG",
    "UNIT_WARRIOR": "UNIT_NAIWA_EGG",
    "UNIT_BUILDER": "UNIT_NAIWA_CHICKEN",
}

tree = ET.parse(SRC)
root = tree.getroot()
rc = root.find("m_RootCollections")
units_coll = None
for el in rc.findall("Element"):
    name = el.find("m_CollectionName")
    if name is not None and name.get("text") == "Units":
        units_coll = el
        break
assert units_coll is not None, "Units root collection not found"

found = {}
for el in list(units_coll.findall("Element")):
    nm = el.find("m_Name")
    if nm is not None and nm.get("text") in RENAME:
        found[nm.get("text")] = el
assert set(found) == set(RENAME), f"缺条目: {set(RENAME) - set(found)}"

out = ET.Element("AssetObjects..ArtDefSet")
ver = ET.SubElement(out, "m_Version")
for tag, val in (("major", "1"), ("minor", "0"), ("build", "0"), ("revision", "0")):
    e = ET.SubElement(ver, tag)
    e.text = val
tpl = ET.SubElement(out, "m_TemplateName")
tpl.set("text", "Units")
orc = ET.SubElement(out, "m_RootCollections")
coll = ET.SubElement(orc, "Element")
cn = ET.SubElement(coll, "m_CollectionName")
cn.set("text", "Units")
rep = ET.SubElement(coll, "m_ReplaceMergedCollectionElements")
rep.text = "false"
for old, new in RENAME.items():
    el = found[old]
    el.find("m_Name").set("text", new)
    coll.append(el)

ET.indent(out, space="  ")
xml = ET.tostring(out, encoding="unicode")
with open(DST, "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8" ?>\n' + xml + "\n")
print("written", DST, "entries:", list(RENAME.values()))
