# Kodi Debug Logging Guide

## How to Enable Debug Logging

### Method 1: Via Kodi Settings (Easiest)

1. In Kodi, go to **Settings** (gear icon)
2. Navigate to **System** → **Logging**
3. Enable **Enable debug logging**
4. Optional but recommended: Enable **Log add-on setting reads**
5. Try to activate the Aurion skin (this will trigger the error)
6. Go back to **Settings** → **System** → **Logging**
7. Click **View log file** (or use Method 2 below to find it)

### Method 2: Find Log File Manually

The log file location depends on your OS:

**Windows:**
```
%APPDATA%\Kodi\kodi.log
```
Full path usually:
```
C:\Users\YOUR_USERNAME\AppData\Roaming\Kodi\kodi.log
```

**Linux:**
```
~/.kodi/temp/kodi.log
```

**macOS:**
```
~/Library/Logs/kodi.log
```

**Android:**
```
/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/temp/kodi.log
```

### Method 3: Via advancedsettings.xml (Advanced)

If you can't access Kodi UI, create/edit this file:

**Windows:** `%APPDATA%\Kodi\userdata\advancedsettings.xml`

```xml
<advancedsettings>
  <loglevel>1</loglevel>
  <showloginfo>true</showloginfo>
</advancedsettings>
```

Restart Kodi after creating this file.

## What to Look For

Search the log file for these keywords:

1. **"skinshortcuts"** - All script.skinshortcuts activity
2. **"Unable to build menu"** - The exact error message
3. **"ERROR"** - Any errors during skin load
4. **"Home.xml"** - Issues parsing Home.xml
5. **"template"** - Template-related errors
6. **"PersonalWidget"** - The specific templates we commented out

### Expected Relevant Log Sections

When script.skinshortcuts runs, you should see lines like:
```
[script.skinshortcuts] Building menu with mainmenuID=9000
[script.skinshortcuts] Processing group: mainmenu
[script.skinshortcuts] Loading shortcuts from: shortcuts/mainmenu.DATA.xml
```

If there's an error, you'll see:
```
ERROR <general>: Error parsing Home.xml
ERROR <general>: Unable to build menu
ERROR <general>: [Specific error detail here]
```

## Sharing the Log

If you need to share the log:

1. **Copy relevant sections** (around the error, ~50 lines before and after)
2. Use a pastebin service: https://paste.kodi.tv/
3. Or save to a file and share

## Quick Terminal Commands

**Windows (PowerShell):**
```powershell
# View log file
notepad "$env:APPDATA\Kodi\kodi.log"

# Search for errors
Select-String -Path "$env:APPDATA\Kodi\kodi.log" -Pattern "skinshortcuts|ERROR|Unable to build" | Select-Object -Last 50
```

**Linux/WSL:**
```bash
# View log file
less ~/.kodi/temp/kodi.log

# Search for errors
grep -i "skinshortcuts\|error\|unable to build" ~/.kodi/temp/kodi.log | tail -50
```

## What to Do After Getting the Log

1. Look for the **first ERROR** related to skinshortcuts or Home.xml
2. Note the **line number** and **file name** if mentioned
3. Check if it's still complaining about the templates we commented out
4. Look for any **XML parsing errors** in shortcuts/*.xml files

## Alternative: Component-Specific Logging

You can enable logging just for script.skinshortcuts:

Edit: `%APPDATA%\Kodi\userdata\addon_data\script.skinshortcuts\settings.xml`

Add:
```xml
<setting id="debugging">true</setting>
```

This creates a separate log file in the addon_data directory with more details.
