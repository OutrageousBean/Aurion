import importlib

import xbmcaddon
import xbmcgui

ADDON = xbmcaddon.Addon()


def have_openscrapers():
    try:
        importlib.import_module("resources.lib.modules.openscrapers")
        return True
    except ImportError:
        try:
            importlib.import_module("openscrapers")
            return True
        except ImportError:
            return False
    except Exception:
        return False


def get_sources(query, media_type, use_rd):
    """
    Build a list of stream sources for the requested media.
    """
    use_os = ADDON.getSettingBool("use_openscrapers") and have_openscrapers()
    if use_os:
        try:
            # Placeholder for OpenScrapers integration.
            # Example:
            # sources = openscrapers.query(
            #     query,
            #     media_type,
            #     debrid=use_rd,
            #     timeout=ADDON.getSettingInt("timeout"),
            # )
            # return [{"label": s["host"], "url": s["url"]} for s in sources]
            pass
        except Exception:
            xbmcgui.Dialog().notification(
                "Aurion", "OpenScrapers error", xbmcgui.NOTIFICATION_ERROR, 3000
            )

    return [{"label": "Sample 1080p", "url": "https://example.com/stream.mp4"}]
