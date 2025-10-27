#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import json
import sys
import os

ADDON            = xbmcaddon.Addon()
ADDON_ID         = ADDON.getAddonInfo('id')
ADDON_NAME       = ADDON.getAddonInfo('name')
ADDON_VERSION    = ADDON.getAddonInfo('version')
HANDLE           = int(sys.argv[1]) if len(sys.argv) > 1 else -1

AURION_REPO_ID   = "repository.aurion"
AURION_VIDEO_ID  = "plugin.video.aurion"
AURION_SKIN_ID   = "skin.aurion"
AURION_SKIN_NAME = "skin.aurion"  # Kodi setting value for look&feel skin


def log(message, level=xbmc.LOGDEBUG):
    """Log a message to the Kodi log."""
    xbmc.log(f"[{ADDON_ID}] {message}", level)


def jsonrpc(method, params=None):
    """Execute a JSON-RPC call to Kodi."""
    payload = {"jsonrpc":"2.0","id":1,"method":method,"params":params or {}}
    resp = xbmc.executeJSONRPC(json.dumps(payload))
    try:
        return json.loads(resp)
    except Exception:
        return {}


def is_installed(addon_id):
    """Check if an addon is installed."""
    r = jsonrpc("Addons.GetAddonDetails", {"addonid": addon_id, "properties": ["name","version"]})
    return "result" in r


def install_addon(addon_id):
    """Install an add-on and wait for completion."""
    log(f"Installing {addon_id}")
    xbmc.executebuiltin(f'InstallAddon({addon_id})')
    # Wait for installation to complete
    for _ in range(40):
        if is_installed(addon_id):
            return True
        xbmc.sleep(250)
    return is_installed(addon_id)


def set_skin(skin_id):
    """Set the active skin and reload."""
    jsonrpc("Settings.SetSettingValue", {"setting":"lookandfeel.skin", "value":skin_id})
    xbmc.sleep(500)
    xbmc.executebuiltin('ReloadSkin()')


def write_skin_defaults():
    """Write default skin settings for Aurion."""
    settings_path = xbmcvfs.translatePath("special://profile/addon_data/skin.aurion/settings.xml")
    settings_dir = os.path.dirname(settings_path)
    
    if not xbmcvfs.exists(settings_dir):
        xbmcvfs.mkdirs(settings_dir)
    
    if not xbmcvfs.exists(settings_path):
        data = """<settings>
  <setting id="color.theme" value="aurion" />
  <setting id="theme.variant" value="curial" />
</settings>"""
        f = xbmcvfs.File(settings_path, 'w')
        f.write(data)
        f.close()
        log("Written default skin settings")


def first_run_welcome():
    """Show welcome dialog on first run."""
    if ADDON.getSettingBool("firstrun_done"):
        return
    xbmcgui.Dialog().ok("Aurion Wizard", "Welcome to Aurion.\nWe'll set up your repo, add-ons, and skin.")
    ADDON.setSettingBool("firstrun_done", True)


def do_setup():
    """Run the full Aurion setup."""
    progress = xbmcgui.DialogProgress()
    progress.create("Aurion Setup", "Setting up Aurion...")
    
    ok = True
    
    # Ensure repo first (lets subsequent installs come from your repo)
    progress.update(25, "Installing Aurion Repository...")
    if not is_installed(AURION_REPO_ID):
        ok &= install_addon(AURION_REPO_ID)
    
    # Ensure video add-on
    progress.update(50, "Installing Aurion Video Plugin...")
    if not is_installed(AURION_VIDEO_ID):
        ok &= install_addon(AURION_VIDEO_ID)
    
    # Ensure skin
    progress.update(75, "Installing Aurion Skin...")
    if not is_installed(AURION_SKIN_ID):
        ok &= install_addon(AURION_SKIN_ID)
    
    # Write skin defaults and switch
    if ok:
        progress.update(90, "Configuring skin...")
        write_skin_defaults()
        set_skin(AURION_SKIN_NAME)
        progress.update(100, "Setup complete!")
        xbmc.sleep(1000)
        progress.close()
        xbmcgui.Dialog().notification("Aurion Wizard", "Setup complete", xbmcgui.NOTIFICATION_INFO, 3000)
    else:
        progress.close()
        xbmcgui.Dialog().notification("Aurion Wizard", "Some items failed to install", xbmcgui.NOTIFICATION_ERROR, 4000)


def update_all():
    """Trigger repository update and check for updates."""
    xbmc.executebuiltin('UpdateAddonRepos')
    xbmc.sleep(1500)
    xbmc.executebuiltin('UpdateLocalAddons')
    xbmcgui.Dialog().notification("Aurion", "Checking for updates...", xbmcgui.NOTIFICATION_INFO, 3000)


def clear_packages_cache():
    """Clear the packages cache directory."""
    packages_path = xbmcvfs.translatePath('special://home/addons/packages/')
    
    if xbmcgui.Dialog().yesno(
        "Clear Packages Cache",
        "This will remove downloaded add-on packages to free up space.",
        "Do you want to continue?"
    ):
        try:
            if xbmcvfs.exists(packages_path):
                dirs, files = xbmcvfs.listdir(packages_path)
                for filename in files:
                    file_path = os.path.join(packages_path, filename)
                    try:
                        xbmcvfs.delete(file_path)
                    except Exception as e:
                        log(f"Error deleting {file_path}: {e}", xbmc.LOGERROR)
                
                xbmcgui.Dialog().notification("Aurion", "Packages cache cleared successfully", xbmcgui.NOTIFICATION_INFO, 3000)
                log("Packages cache cleared")
            else:
                xbmcgui.Dialog().notification("Aurion", "Packages directory not found", xbmcgui.NOTIFICATION_WARNING, 3000)
        except Exception as e:
            log(f"Error clearing packages cache: {e}", xbmc.LOGERROR)
            xbmcgui.Dialog().ok("Error", f"Failed to clear packages cache: {str(e)}")


def build_menu():
    """Build the main wizard menu."""
    li1 = xbmcgui.ListItem("➤ Run Setup (install repo, video, skin)")
    xbmcplugin.addDirectoryItem(HANDLE, f'plugin://{ADDON_ID}?action=setup', li1, isFolder=False)

    li2 = xbmcgui.ListItem("⟳ Update Aurion Add-ons")
    xbmcplugin.addDirectoryItem(HANDLE, f'plugin://{ADDON_ID}?action=update', li2, isFolder=False)

    li3 = xbmcgui.ListItem("🗑️ Clear Packages Cache")
    xbmcplugin.addDirectoryItem(HANDLE, f'plugin://{ADDON_ID}?action=clear_cache', li3, isFolder=False)

    li4 = xbmcgui.ListItem("ℹ Welcome / About")
    xbmcplugin.addDirectoryItem(HANDLE, f'plugin://{ADDON_ID}?action=welcome', li4, isFolder=False)

    xbmcplugin.endOfDirectory(HANDLE)


def router():
    """Route the action based on query string."""
    import urllib.parse as urlparse
    qs = {}
    if len(sys.argv) > 2 and sys.argv[2]:
        qs = dict(urlparse.parse_qsl(sys.argv[2][1:]))

    action = qs.get('action')
    if action == 'setup':
        first_run_welcome()
        do_setup()
    elif action == 'update':
        update_all()
    elif action == 'clear_cache':
        clear_packages_cache()
    elif action == 'welcome':
        first_run_welcome()
        xbmcgui.Dialog().ok("Aurion", "Aurion is installed.\nUse the Update option anytime.")
    else:
        build_menu()


if __name__ == '__main__':
    log(f"{ADDON_NAME} v{ADDON_VERSION} started")
    router()
