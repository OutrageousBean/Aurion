import xbmc
import xbmcgui

home = xbmcgui.Window(10000)
skin = home.getProperty("CurrentSkin")
if skin == "skin.aurion":
    xbmc.executebuiltin("SetFocus(8000)")
