import os
import zipfile
import pathlib
import xml.etree.ElementTree as ET
import hashlib

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
    # Create zip in addon_id subdirectory
    out_path = out_dir / addon_id / f"{addon_id}-{version}.zip"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create zip with addon files in correct structure
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        base_name = addon_path.name
        for folder, _, files in os.walk(addon_path):
            rel_folder = pathlib.Path(folder).relative_to(addon_path.parent)
            for file in files:
                full_path = pathlib.Path(folder) / file
                # Ensure files go into addon_id directory in zip
                arc_path = rel_folder / file
                zipf.write(full_path, arc_path)
    
    return addon_id, version

def generate_md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def generate_addons_xml():
    addons = []
    # Add repository addon first
    if (REPO / "addon.xml").exists():
        addons.append((REPO / "addon.xml").read_text())
    
    # Add all other addons
    for addon in ADDONS.iterdir():
        if addon.is_dir():
            xml_path = addon / "addon.xml"
            if xml_path.exists():
                addons.append(xml_path.read_text())
    
    # Write addons.xml
    xml_content = "<addons>\n" + "\n".join(addons) + "\n</addons>"
    addons_xml = ROOT / "addons.xml"
    addons_xml.write_text(xml_content, encoding='utf-8')
    
    # Generate proper MD5
    md5_path = ROOT / "addons.xml.md5"
    md5_path.write_text(generate_md5(addons_xml))

def main():
    print("Building Aurion Repository...")
    
    # Ensure zips directory exists
    ZIPS.mkdir(exist_ok=True)
    
    # Build repository addon first
    print("Building repository addon...")
    zip_addon(REPO, ZIPS)
    
    # Build all other addons
    print("Building addons...")
    for addon in ADDONS.iterdir():
        if addon.is_dir():
            addon_id, version = zip_addon(addon, ZIPS)
            print(f"Built {addon_id} version {version}")
    
    # Generate addons.xml and MD5
    print("Generating addons.xml and MD5...")
    generate_addons_xml()
    
    print("Build complete!")

if __name__ == "__main__":
    main()
