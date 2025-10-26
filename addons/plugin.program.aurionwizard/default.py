#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os
import shutil

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_VERSION = ADDON.getAddonInfo('version')


def log(message, level=xbmc.LOGDEBUG):
    """Log a message to the Kodi log."""
    xbmc.log(f"[{ADDON_ID}] {message}", level)


def show_notification(message, title=ADDON_NAME, time=5000, icon=None):
    """Show a notification to the user."""
    if icon is None:
        icon = ADDON.getAddonInfo('icon')
    xbmcgui.Dialog().notification(title, message, icon, time)


def show_message(heading, message):
    """Show an OK dialog."""
    xbmcgui.Dialog().ok(heading, message)


def install_addon(addon_id):
    """Install an add-on using the built-in installer."""
    log(f"Attempting to install {addon_id}")
    show_notification(f"Installing {addon_id}...", time=3000)
    xbmc.executebuiltin(f'InstallAddon({addon_id})')
    # Note: InstallAddon is async, so the addon may not be immediately available
    show_notification(f"{addon_id} installation started", time=3000)


def clear_packages_cache():
    """Clear the packages cache directory."""
    packages_path = xbmcvfs.translatePath('special://home/addons/packages/')
    
    if xbmcgui.Dialog().yesno(
        "Clear Packages Cache",
        "This will remove downloaded add-on packages to free up space.",
        "Do you want to continue?"
    ):
        try:
            if os.path.exists(packages_path):
                for filename in os.listdir(packages_path):
                    file_path = os.path.join(packages_path, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        log(f"Error deleting {file_path}: {e}", xbmc.LOGERROR)
                
                show_notification("Packages cache cleared successfully")
                log("Packages cache cleared")
            else:
                show_notification("Packages directory not found", time=3000)
        except Exception as e:
            log(f"Error clearing packages cache: {e}", xbmc.LOGERROR)
            show_message("Error", f"Failed to clear packages cache: {str(e)}")


def open_addon_settings(addon_id):
    """Open the settings dialog for a specific add-on."""
    log(f"Opening settings for {addon_id}")
    xbmc.executebuiltin(f'Addon.OpenSettings({addon_id})')


def apply_skin_defaults():
    """Apply default settings for the Aurion skin."""
    skin_id = 'skin.aurion'
    
    # Check if skin is installed
    try:
        skin_addon = xbmcaddon.Addon(skin_id)
    except RuntimeError:
        if xbmcgui.Dialog().yesno(
            "Skin Not Installed",
            "The Aurion skin is not installed yet.",
            "Would you like to install it first?"
        ):
            install_addon(skin_id)
        return
    
    if xbmcgui.Dialog().yesno(
        "Apply Aurion Skin Defaults",
        "This will apply recommended default settings for the Aurion skin.",
        "Do you want to continue?"
    ):
        try:
            # Example: Set a few recommended settings
            # You can expand this with your preferred defaults
            skin_addon.setSetting('home_widget_movies', 'true')
            skin_addon.setSetting('home_widget_tvshows', 'true')
            
            show_notification("Skin defaults applied. Reloading skin...")
            log("Applied Aurion skin defaults")
            
            # Reload the skin to apply changes
            xbmc.executebuiltin('ReloadSkin()')
        except Exception as e:
            log(f"Error applying skin defaults: {e}", xbmc.LOGERROR)
            show_message("Error", f"Failed to apply skin defaults: {str(e)}")


def show_main_menu():
    """Display the main wizard menu."""
    options = [
        "Install Aurion Skin",
        "Install Aurion Video Add-on",
        "Apply Aurion Skin Defaults",
        "Open Aurion Skin Settings",
        "Clear Packages Cache",
        "About"
    ]
    
    dialog = xbmcgui.Dialog()
    choice = dialog.select(f"{ADDON_NAME} v{ADDON_VERSION}", options)
    
    if choice == 0:
        install_addon('skin.aurion')
    elif choice == 1:
        install_addon('plugin.video.aurion')
    elif choice == 2:
        apply_skin_defaults()
    elif choice == 3:
        open_addon_settings('skin.aurion')
    elif choice == 4:
        clear_packages_cache()
    elif choice == 5:
        show_message(
            f"{ADDON_NAME} v{ADDON_VERSION}",
            "Aurion Setup and Maintenance Wizard\n\n"
            "This wizard helps you install and configure Aurion add-ons.\n\n"
            "Created by OutrageousBean"
        )


if __name__ == '__main__':
    log(f"{ADDON_NAME} v{ADDON_VERSION} started")
    show_main_menu()
