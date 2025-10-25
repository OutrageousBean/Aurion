import os, zipfile, pathlib, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADDONS = ROOT / "addons"
REPO = ROOT / "repository.aurion"
ZIPS = ROOT / "zips"

def get_addon_info(addon_path):
    xml = addon_path / "addon.xml"
    tree = ET.parse(xml)
    elem = tree.getroot()
    return elem.attrib['id'], elem.attrib['version']

def zip_addon(addon_path, out_dir):
    addon_id, version = get_addon_info(addon_path)
    out_path = out_dir / addon_id / f"{addon_id}-{version}.zip"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder, _, files in os.walk(addon_path):
            for file in files:
                full = pathlib.Path(folder) / file
                zipf.write(full, full.relative_to(addon_path.parent))
    return addon_id, version

def generate_addons_xml():
    addons = []
    for addon in ADDONS.iterdir():
        if addon.is_dir():
            xml_path = addon / "addon.xml"
            if xml_path.exists():
                addons.append(xml_path.read_text())
    REPO_XML = ROOT / "addons.xml"
    REPO_XML.write_text("<addons>\n" + "\n".join(addons) + "\n</addons>")
    (ROOT / "addons.xml.md5").write_text(str(hash(REPO_XML.read_text())))

def main():
    ZIPS.mkdir(exist_ok=True)
    for addon in ADDONS.iterdir():
        if addon.is_dir():
            zip_addon(addon, ZIPS)
    zip_addon(REPO, ZIPS)
    generate_addons_xml()

if __name__ == "__main__":
    main()
