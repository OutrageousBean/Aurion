import sys
import urllib.parse as urlparse

import xbmcaddon
import xbmcgui
import xbmcplugin

from resources.lib import providers

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]


def build_url(**qs):
    return BASE_URL + "?" + urlparse.urlencode(qs)


def list_root():
    items = [
        ("Movies", {"action": "movies"}),
        ("TV Shows", {"action": "tvshows"}),
        ("Search", {"action": "search"}),
        ("Accounts", {"action": "accounts"}),
    ]
    xbmcplugin.setPluginCategory(HANDLE, "Aurion")
    xbmcplugin.setContent(HANDLE, "addons")
    for label, query in items:
        list_item = xbmcgui.ListItem(label=label)
        xbmcplugin.addDirectoryItem(HANDLE, build_url(**query), list_item, isFolder=True)
    xbmcplugin.endOfDirectory(HANDLE)


def route_movies():
    # stubs; to be replaced with provider calls
    xbmcplugin.setPluginCategory(HANDLE, "Aurion Movies")
    xbmcplugin.setContent(HANDLE, "videos")
    for label, action in [("Trending", "trending"), ("Popular", "popular")]:
        list_item = xbmcgui.ListItem(label)
        xbmcplugin.addDirectoryItem(
            HANDLE, build_url(action=action, type="movie"), list_item, True
        )
    xbmcplugin.endOfDirectory(HANDLE)


def route_tv():
    xbmcplugin.setPluginCategory(HANDLE, "Aurion TV")
    xbmcplugin.setContent(HANDLE, "videos")
    for label, action in [("Trending", "trending"), ("Popular", "popular")]:
        list_item = xbmcgui.ListItem(label)
        xbmcplugin.addDirectoryItem(
            HANDLE, build_url(action=action, type="tv"), list_item, True
        )
    xbmcplugin.endOfDirectory(HANDLE)


def route_search(initial=None, media_type=None):
    if initial:
        show_results(query=initial, media_type=media_type)
        return
    keyboard = xbmcgui.Dialog().input("Search", type=xbmcgui.INPUT_ALPHANUM)
    if not keyboard:
        xbmcplugin.endOfDirectory(HANDLE)
        return
    show_results(query=keyboard, media_type=media_type)


def show_results(query=None, media_type=None, action=None):
    # placeholder list—wire to providers later
    label = query or action or "Item"
    xbmcplugin.setPluginCategory(HANDLE, f"Aurion {label.title()}")
    xbmcplugin.setContent(HANDLE, "videos")
    for index in range(1, 11):
        list_item = xbmcgui.ListItem(f"{label} {index}")
        list_item.setInfo("video", {"title": f"{label} {index}"})
        list_item.setProperty("IsPlayable", "true")
        # When sources are ready, set URL to a resolver path
        xbmcplugin.addDirectoryItem(
            HANDLE,
            build_url(
                action="play",
                id=str(index),
                type=media_type or "",
                query=label,
            ),
            list_item,
            isFolder=False,
        )
    xbmcplugin.endOfDirectory(HANDLE)


def open_accounts():
    list_item = xbmcgui.ListItem("Authorize Real-Debrid")
    xbmcplugin.addDirectoryItem(HANDLE, build_url(action="rd_auth"), list_item, isFolder=False)
    xbmcplugin.endOfDirectory(HANDLE)


def rd_device_auth():
    # Opens ResolveURL settings if present; otherwise direct device flow later
    try:
        xbmcaddon.Addon("script.module.resolveurl").openSettings()
    except Exception:
        xbmcgui.Dialog().ok(
            "Aurion", "ResolveURL not installed.\nYou can still use non-RD providers."
        )


def play_item():
    # later: collect sources -> optionally RD -> resolve -> setResolvedUrl
    query = dict(urlparse.parse_qsl(sys.argv[2][1:])) if len(sys.argv) > 2 else {}
    media_type = query.get("type") or "video"
    search_term = query.get("query") or ""
    use_rd = ADDON.getSettingBool("rd_enabled")
    sources = providers.get_sources(search_term, media_type, use_rd)
    if not sources:
        xbmcgui.Dialog().notification("Aurion", "No sources found", xbmcgui.NOTIFICATION_WARNING, 3000)
        xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
        return

    if len(sources) == 1:
        selected = sources[0]
    else:
        choice = xbmcgui.Dialog().select("Choose source", [s.get("label", "Source") for s in sources])
        if choice == -1:
            xbmcplugin.setResolvedUrl(HANDLE, False, xbmcgui.ListItem())
            return
        selected = sources[choice]

    list_item = xbmcgui.ListItem(path=selected.get("url", ""))
    list_item.setProperty("IsPlayable", "true")
    xbmcplugin.setResolvedUrl(HANDLE, True, list_item)


def router():
    query = dict(urlparse.parse_qsl(sys.argv[2][1:])) if len(sys.argv) > 2 else {}
    action = query.get("action")
    if action is None:
        list_root()
    elif action == "movies":
        route_movies()
    elif action == "tvshows":
        route_tv()
    elif action == "search":
        route_search(query.get("query"), query.get("type"))
    elif action in ("trending", "popular"):
        show_results(action=action, media_type=query.get("type"))
    elif action == "accounts":
        open_accounts()
    elif action == "rd_auth":
        rd_device_auth()
    elif action == "play":
        play_item()
    else:
        list_root()


if __name__ == "__main__":
    router()
