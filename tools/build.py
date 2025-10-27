import os
import re
import zipfile
import pathlib
import xml.etree.ElementTree as ET
import hashlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADDONS = ROOT / "addons"
REPO = ROOT / "repository.aurion"
DOCS = ROOT / "docs"
ZIPS = DOCS / "zips"

def write_file(path: pathlib.Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

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
        for folder, _, files in os.walk(addon_path):
            rel_path = pathlib.Path(folder).relative_to(addon_path)
            zip_folder = pathlib.Path(addon_id) / rel_path
            for file in files:
                file_path = pathlib.Path(folder) / file
                arc_path = zip_folder / file
                print(f"Adding {file_path} as {arc_path}")
                zipf.write(file_path, arc_path)
    
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
        content = (REPO / "addon.xml").read_text()
        # Strip any XML declaration like <?xml ...?> anywhere in the file
        content = re.sub(r"\s*<\?xml[^>]*\?>", "", content, flags=re.IGNORECASE)
        content = content.strip()
        addons.append(content)
    
    # Add all other addons
    for addon in ADDONS.iterdir():
        if addon.is_dir():
            xml_path = addon / "addon.xml"
            if xml_path.exists():
                content = xml_path.read_text()
                # Strip any XML declaration like <?xml ...?> anywhere in the file
                content = re.sub(r"\s*<\?xml[^>]*\?>", "", content, flags=re.IGNORECASE)
                content = content.strip()
                addons.append(content)
    
    # Write addons.xml with proper XML declaration
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n' + "\n".join(addons) + "\n</addons>"
    addons_xml = DOCS / "addons.xml"
    addons_xml.write_text(xml_content, encoding='utf-8')
    
    # Generate proper MD5
    md5_path = DOCS / "addons.xml.md5"
    md5_hash = generate_md5(addons_xml)
    md5_path.write_text(md5_hash, encoding='utf-8')

def generate_html_index_pages():
        """
        Generate simple HTML directory listings so Kodi can browse HTTP sources.
        Creates:
            - docs/index.html
            - docs/zips/index.html
            - docs/zips/<addon_id>/index.html
        """
        # docs/index.html
        root_index = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>Aurion Repository</title>
    <style>
        body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding: 24px; line-height: 1.5; }}
        a {{ color: #0b69ff; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        ul {{ list-style: none; padding-left: 0; }}
        li {{ margin: 6px 0; }}
        code {{ background: #f5f7fa; padding: 2px 6px; border-radius: 4px; }}
    </style>
    <meta http-equiv=\"Cache-Control\" content=\"no-cache, no-store, must-revalidate\" />
    <meta http-equiv=\"Pragma\" content=\"no-cache\" />
    <meta http-equiv=\"Expires\" content=\"0\" />
    <base href=\"./\" />
    <link rel=\"canonical\" href=\"./\" />
    <meta name=\"robots\" content=\"all\" />
    <meta name=\"description\" content=\"Aurion Kodi repository files\" />
    <meta name=\"format-detection\" content=\"telephone=no\" />
    <meta name=\"referrer\" content=\"no-referrer-when-downgrade\" />
    <meta http-equiv=\"x-dns-prefetch-control\" content=\"on\" />
    <link rel=\"dns-prefetch\" href=\"//outrageousbean.github.io\" />
    <link rel=\"dns-prefetch\" href=\"//github.io\" />
    <link rel=\"dns-prefetch\" href=\"//github.com\" />
    <meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; style-src 'self' 'unsafe-inline'\" />
    <meta http-equiv=\"Cross-Origin-Opener-Policy\" content=\"same-origin\" />
    <meta http-equiv=\"Cross-Origin-Embedder-Policy\" content=\"require-corp\" />
    <meta http-equiv=\"Cross-Origin-Resource-Policy\" content=\"same-origin\" />
    <meta http-equiv=\"Permissions-Policy\" content=\"geolocation=()\" />
    <meta http-equiv=\"Referrer-Policy\" content=\"no-referrer-when-downgrade\" />
    <meta http-equiv=\"X-Content-Type-Options\" content=\"nosniff\" />
    <meta http-equiv=\"X-Frame-Options\" content=\"DENY\" />
    <meta http-equiv=\"X-XSS-Protection\" content=\"1; mode=block\" />
    <meta name=\"color-scheme\" content=\"light dark\" />
    <meta name=\"theme-color\" content=\"#111827\" />
    <meta name=\"supported-color-schemes\" content=\"light dark\" />
    <meta name=\"browsermode\" content=\"application\" />
    <meta name=\"HandheldFriendly\" content=\"true\" />
    <meta name=\"MobileOptimized\" content=\"320\" />
    <meta name=\"apple-mobile-web-app-capable\" content=\"yes\" />
    <meta name=\"apple-mobile-web-app-status-bar-style\" content=\"black\" />
    <meta name=\"apple-mobile-web-app-title\" content=\"Aurion Repo\" />
    <meta name=\"application-name\" content=\"Aurion Repo\" />
    <meta name=\"msapplication-TileColor\" content=\"#2b5797\" />
    <meta name=\"msapplication-tap-highlight\" content=\"no\" />
    <meta name=\"msapplication-config\" content=\"none\" />
    <meta name=\"format-detection\" content=\"address=no\" />
    <meta name=\"renderer\" content=\"webkit\" />
    <meta name=\"force-rendering\" content=\"webkit\" />
    <meta name=\"Referrer\" content=\"no-referrer\" />
    <meta name=\"referrer\" content=\"no-referrer\" />
    <meta name=\"viewport-fit\" content=\"cover\" />
    <meta name=\"apple-mobile-web-app-status-bar-style\" content=\"default\" />
    <meta name=\"generator\" content=\"Aurion build.py\" />
    <meta name=\"author\" content=\"Aurion\" />
    <meta name=\"owner\" content=\"Aurion\" />
    <meta name=\"publisher\" content=\"Aurion\" />
    <meta name=\"copyright\" content=\"Copyright (c) Aurion\" />
    <meta name=\"rating\" content=\"General\" />
    <meta name=\"revisit-after\" content=\"7 days\" />
    <meta name=\"distribution\" content=\"global\" />
    <meta name=\"coverage\" content=\"Worldwide\" />
    <meta name=\"target\" content=\"all\" />
    <meta name=\"audience\" content=\"all\" />
    <meta name=\"page-topic\" content=\"Software\" />
    <meta name=\"Page-Type\" content=\"Index\" />
    <meta name=\"doc-class\" content=\"Public\" />
    <meta name=\"doc-rights\" content=\"Public\" />
    <meta name=\"doc-type\" content=\"Public\" />
    <meta name=\"doc-rating\" content=\"General\" />
    <meta name=\"language\" content=\"en\" />
    <meta name=\"charset\" content=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <meta name=\"keywords\" content=\"Kodi, Repository, Aurion\" />
    <meta name=\"description\" content=\"Aurion Kodi repository directory\" />
    <meta http-equiv=\"refresh\" content=\"0; url=zips/\" />
    <noscript>
        <meta http-equiv=\"refresh\" content=\"0; url=zips/\" />
    </noscript>
    <link rel=\"alternate\" type=\"application/xml\" href=\"addons.xml\" />
</head>
<body>
    <h1>Aurion Repository</h1>
    <ul>
        <li><a href=\"addons.xml\">addons.xml</a></li>
        <li><a href=\"addons.xml.md5\">addons.xml.md5</a></li>
        <li><a href=\"zips/\">zips/</a></li>
    </ul>
    <p>If you opened this in Kodi, go into <strong>zips/</strong> to browse.</p>
</body>
</html>
"""
        write_file(DOCS / "index.html", root_index)

        # docs/zips/index.html
        addon_dirs = []
        if ZIPS.exists():
                for item in sorted(ZIPS.iterdir()):
                        if item.is_dir():
                                addon_dirs.append(item.name)
        zips_index = [
                "<!DOCTYPE html>",
                "<html lang=\"en\"><head><meta charset=\"UTF-8\"><title>zips/</title></head><body>",
                "<h1>zips/</h1>",
                "<ul>",
        ]
        for name in addon_dirs:
                zips_index.append(f"  <li><a href=\"{name}/\">{name}/</a></li>")
        zips_index += [
                "</ul>",
                "</body></html>",
        ]
        write_file(ZIPS / "index.html", "\n".join(zips_index))

        # docs/zips/<addon_id>/index.html
        for name in addon_dirs:
                subdir = ZIPS / name
                files = [p.name for p in sorted(subdir.iterdir()) if p.is_file()]
                sub_lines = [
                        "<!DOCTYPE html>",
                        f"<html lang=\"en\"><head><meta charset=\"UTF-8\"><title>{name}/</title></head><body>",
                        f"<h1>{name}/</h1>",
                        "<ul>",
                ]
                for fname in files:
                        sub_lines.append(f"  <li><a href=\"{fname}\">{fname}</a></li>")
                sub_lines += [
                        "</ul>",
                        "</body></html>",
                ]
                write_file(subdir / "index.html", "\n".join(sub_lines))

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
            try:
                addon_id, version = zip_addon(addon, ZIPS)
                print(f"Built {addon_id} version {version}")
            except Exception as e:
                # Log and continue so addons.xml/MD5 still regenerate
                print(f"Warning: failed to build {addon.name}: {e}")
    
    # Generate addons.xml and MD5
    print("Generating addons.xml and MD5...")
    generate_addons_xml()
    
    # Generate HTML indexes for HTTP browsing
    print("Generating HTML index pages...")
    generate_html_index_pages()
    
    print("Build complete!")

if __name__ == "__main__":
    main()
