import xbmcplugin, xbmcgui, sys

def main():
    handle = int(sys.argv[1])
    xbmcplugin.setPluginCategory(handle, "Aurion")
    xbmcplugin.addDirectoryItem(handle, url="", listitem=xbmcgui.ListItem("Coming soon..."), isFolder=False)
    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
