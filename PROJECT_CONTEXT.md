# Aurion Kodi Addon - Project Context & Status

## Project Overview

**Aurion** is a custom Kodi addon package consisting of two main components:
- **skin.aurion**: A custom Kodi skin theme based on Estuary MOD V2
- **plugin.video.aurion**: A video plugin addon for content integration

The project is distributed via a self-hosted GitHub Pages repository that users can install directly into Kodi.

## Project Goals

1. Create a polished, feature-rich Kodi skin with custom branding
2. Integrate a video plugin that provides curated content (trending movies/TV)
3. Add custom UI elements:
   - Custom header bar with logo and action buttons
   - "Spotlight" horizontal scrolling rows for featured content
4. Distribute via self-hosted repository for easy installation and updates

## Technology Stack

- **Platform**: Kodi Omega (21.x)
- **Base Skin**: Estuary MOD V2 (fork)
- **Languages**: XML (UI), Python (plugin logic)
- **Distribution**: GitHub Pages (static hosting)
- **Build System**: Custom Python build script (`tools/build.py`)
- **Version Control**: Git + SSH authentication

## Architecture

### Repository Structure
```
Aurion/
├── addons/
│   ├── plugin.video.aurion/          # Video content plugin
│   ├── script.skinshortcuts/         # Menu management addon (dependency)
│   └── skin.aurion/                  # Main skin theme
│       ├── xml/                      # UI layouts and includes
│       ├── media/                    # Textures and assets
│       ├── colors/                   # Color schemes
│       ├── shortcuts/                # Menu definitions (*.DATA.xml)
│       ├── language/                 # Internationalization
│       └── scripts/                  # Python helper scripts
├── repository.aurion/                # Repository metadata addon
├── tools/
│   └── build.py                      # Packaging script
└── docs/                             # GitHub Pages output
    ├── addons.xml                    # Repository manifest
    └── zips/                         # Installable addon packages
```

### Key Technologies

**Kodi Skinning System:**
- XML-based UI definition language
- Conditional visibility expressions
- Include system for reusable components
- Animation engine
- InfoLabels for dynamic data binding

**script.skinshortcuts:**
- Third-party addon that manages main menu and widget system
- Parses `shortcuts/*.DATA.xml` files to build menu structure
- Generates dynamic control IDs and layouts
- Templates: PersonalWidgetList, PersonalWidgetPanel, PersonalWidgetVariable

**GitHub Pages Distribution:**
- Static file hosting via `docs/` directory
- `addons.xml` manifest lists all available addons
- MD5 checksums for integrity verification
- Kodi reads repository like official repos

## Current Implementation Status

### ✅ Completed Features

1. **Logo Positioning** (omega.31-33)
   - Custom header bar defined in `Includes.xml`
   - Logo sized at 256x64px, positioned at left=0, top=16
   - Search/Update buttons positioned at left=320
   - Uses `special://skin/media/icon.png` for texture path

2. **Plugin Fallback Art** (plugin 1.0.3)
   - Video plugin returns placeholder content
   - Implements `DefaultVideo.png` fallback for artwork
   - Routes defined for trending movies and TV shows

3. **AurionSpotlight Include** (Includes_Home.xml)
   - Reusable spotlight component defined
   - Horizontal scrolling panel with poster layout
   - Parameterized for label, content path, and panel ID
   - Position: top=600, left=60, right=60, height=420

4. **Repository Infrastructure**
   - Self-hosted GitHub Pages repository functional
   - Build script generates zips and metadata
   - Version bumping and cache refresh mechanisms
   - script.skinshortcuts 2.0.3 included in repository

5. **Dependency Management**
   - xbmc.gui updated to 5.17.0 (Kodi Omega requirement)
   - All skin dependencies declared in addon.xml
   - script.skinshortcuts dependencies satisfied (simpleeval, unidecode)

### ❌ Blocked Features

1. **AurionHeaderBar Integration**
   - **Status**: Defined but NOT integrated
   - **Reason**: Causes toolbar formatting issues when added to Home.xml
   - **Location**: `addons/skin.aurion/xml/Includes.xml` (lines with logo/buttons)
   - **Intended Use**: Custom header with logo and action buttons on home screen

2. **Spotlight Rows Integration**
   - **Status**: Defined but NOT integrated
   - **Reason**: 
     - Invisible when placed inside group 2000
     - Breaks toolbar when placed outside group 2000
     - Conflicts with skinshortcuts menu builder
   - **Location**: `addons/skin.aurion/xml/Includes_Home.xml` (AurionSpotlight include)
   - **Intended Use**: Two horizontal scrolling rows (Movies + TV) on home screen

### 🔴 Critical Blocker

**"Unable to build menu" Error**

- **Source**: script.skinshortcuts addon
- **Trigger**: When attempting to load Aurion skin
- **Persists**: Even after complete revert to base skin (omega.38)
- **Impact**: Skin completely unusable - cannot activate

**What Makes This Critical:**
- Error exists in CLEAN state (no custom modifications)
- All dependencies are installed and satisfied
- Error persists through clean reinstall and Kodi restart
- Prevents any further development or testing

## Development Timeline

### Phase 1: Setup & Logo Fix (Versions omega.31-33)
- Fixed header logo sizing and positioning
- Resolved texture path issues
- Multiple build/deploy iterations

### Phase 2: Feature Implementation (Version omega.34)
- Implemented Spotlight rows in Home.xml
- Updated plugin to return proper artwork
- Features invisible on first deployment

### Phase 3: Visibility Debugging (Versions omega.35-36)
- Removed visibility conditions
- Adjusted positioning
- Moved elements outside skinshortcuts-managed group
- Repository cache refresh issues

### Phase 4: Dependency Resolution (Version omega.37)
- Fixed xbmc.gui version mismatch
- Attempted to resolve skinshortcuts conflicts
- Toolbar formatting broke when moving header bar

### Phase 5: Isolation & Debugging (Version omega.38 - CURRENT)
- Complete revert of all custom additions
- Added script.skinshortcuts to repository
- Menu build error persists in clean state
- **BLOCKED ON ROOT CAUSE IDENTIFICATION**

## Technical Challenges Encountered

### 1. Skinshortcuts Integration Fragility
- script.skinshortcuts expects very specific Home.xml structure
- Group 2000 is exclusively managed by skinshortcuts templates
- Any modifications break menu generation
- Documentation sparse on how to safely extend

### 2. Visibility/Positioning Issues
- Custom controls invisible when inside skinshortcuts-managed groups
- Custom controls break formatting when outside those groups
- Conditional visibility system complex and poorly documented

### 3. Repository Distribution
- Kodi caching aggressive - version bumps don't always propagate
- Dependency auto-installation only works for official Kodi repos
- Custom repo requires manual dependency installation

### 4. Debugging Limitations
- Limited error messages without debug logging enabled
- XML validation tools not available in development environment
- Difficult to trace skinshortcuts internal behavior

## Known Issues & Limitations

1. **Menu Build Failure** (CRITICAL)
   - Root cause unknown
   - May be inherited from base Estuary MOD V2 skin
   - Possibly corrupted shortcuts DATA files
   - Could be skinshortcuts version incompatibility (2.0.3 vs 1.1.6)

2. **Dependency Auto-Installation**
   - Kodi doesn't auto-install dependencies from custom repos
   - Users must manually install script.skinshortcuts
   - Poor user experience

3. **Custom UI Element Integration**
   - No clear path to add header bar or spotlight rows
   - May require completely different approach
   - Alternatives: custom dialogs, overlays, post-build injection

## Environment & Tools

- **Development OS**: Windows (WSL Ubuntu for git/build)
- **Kodi Version**: Omega (21.x)
- **Build System**: Python 3.x with zipfile, xml.etree
- **Git Auth**: SSH with passphrase
- **Validation**: xmllint (not currently available)
- **IDE**: VS Code with GitHub Copilot

## User Workflow (Installation)

Current installation process:
1. Add-ons → Install from zip file
2. Enter URL: `https://outrageousbean.github.io/Aurion/zips/repository.aurion/repository.aurion-1.0.1.zip`
3. Repository installs successfully
4. Add-ons → Install from repository → Aurion Repository → Skin → Aurion
5. **Expected**: Auto-install dependencies and activate skin
6. **Actual**: Dependencies don't auto-install, manual installation needed
7. Manually install script.skinshortcuts from repository
8. Attempt to activate skin
9. **ERROR**: "Unable to build menu" prevents skin activation

## Project Dependencies

### Direct Dependencies
- `xbmc.gui` 5.17.0 (Kodi Omega API)
- `script.skinshortcuts` 1.1.6+ (menu management)
- `plugin.program.autocompletion` 2.0.4 (UI helpers)

### script.skinshortcuts Dependencies
- `script.module.simpleeval` 0.9.10 (expression evaluation)
- `script.module.unidecode` 1.1.1+ (character encoding)

### Development Dependencies
- Python 3.x (build script)
- Git (version control)
- GitHub Pages (hosting)
- WSL/Ubuntu (build environment)

## Next Steps & Priorities

### Immediate (P0 - BLOCKING)
1. **Enable Kodi debug logging and capture actual skinshortcuts error**
   - This is the MOST IMPORTANT step
   - Will reveal exact failure point
   - Should be done before any other troubleshooting

2. **Validate shortcuts DATA files for XML syntax errors**
   - Install xmllint: `sudo apt install libxml2-utils`
   - Run validation on all 13 shortcuts/*.DATA.xml files
   - Fix any malformed XML

3. **Try script.skinshortcuts 1.1.6 instead of 2.0.3**
   - Version mismatch may cause compatibility issues
   - Skin explicitly requires 1.1.6
   - Currently using 2.0.3 (major version jump)

### Short-term (P1)
4. **Compare with working Estuary MOD V2 installation**
   - Download original base skin
   - Verify it works in same Kodi instance
   - Compare shortcuts files and Home.xml structure

5. **Research alternative approaches for custom UI elements**
   - Custom dialog windows
   - Overlay controls
   - Post-skinshortcuts-build injection
   - Different window (not Home)

### Long-term (P2)
6. **Improve dependency distribution**
   - Consider packaging skin as single addon with embedded dependencies
   - Or add dependency installation wizard
   - Better user documentation

7. **Re-implement blocked features once menu build is fixed**
   - AurionHeaderBar integration
   - Spotlight rows integration
   - Test thoroughly before each version bump

## Success Criteria

### Milestone 1: Functional Base Skin
- [ ] Resolve "Unable to build menu" error
- [ ] Skin activates successfully in Kodi
- [ ] All base Estuary MOD V2 features work
- [ ] Menu system navigable

### Milestone 2: Custom Branding
- [ ] AurionHeaderBar displays on home screen
- [ ] Logo visible and correctly positioned
- [ ] Action buttons functional
- [ ] No formatting or layout issues

### Milestone 3: Spotlight Feature
- [ ] Two spotlight rows visible on home
- [ ] Content loads from plugin
- [ ] Horizontal scrolling works
- [ ] Artwork displays correctly
- [ ] No conflicts with skinshortcuts

### Milestone 4: Polish & Distribution
- [ ] Dependency auto-installation working
- [ ] Repository documentation complete
- [ ] Installation instructions clear
- [ ] All features tested and stable

## Code Locations Reference

**Files Currently Modified:**
- `addons/skin.aurion/xml/Includes.xml` (AurionHeaderBar defined but unused)
- `addons/skin.aurion/xml/Includes_Home.xml` (AurionSpotlight defined but unused)
- `addons/skin.aurion/xml/Home.xml` (reverted to clean state)
- `addons/skin.aurion/addon.xml` (version omega.38, dependencies declared)
- `addons/plugin.video.aurion/main.py` (fallback art implemented)
- `repository.aurion/addon.xml` (version 1.0.1)

**Files Needing Investigation:**
- `addons/skin.aurion/shortcuts/*.DATA.xml` (13 files - may be corrupted)
- `addons/skin.aurion/xml/script-skinshortcuts.xml` (skinshortcuts configuration)
- Kodi debug log (need to enable and capture)

**Build Output:**
- `docs/addons.xml` (repository manifest)
- `docs/zips/skin.aurion/` (packaged skin addon)
- `docs/zips/script.skinshortcuts/` (dependency package)
- `docs/zips/plugin.video.aurion/` (plugin package)
- `docs/zips/repository.aurion/` (repository addon)

## Lessons Learned

1. **Skinshortcuts is extremely fragile** - requires deep understanding of its internal workings
2. **Test incrementally** - we should have tested base skin BEFORE adding features
3. **Debug logging essential** - should enable from day one
4. **Version matching matters** - dependency version mismatches cause subtle issues
5. **XML validation critical** - corrupted files can cause cascading failures
6. **Repository caching complex** - Kodi's update mechanism not always reliable

## Resources & References

- **Kodi Skinning Documentation**: https://kodi.wiki/view/Skinning
- **Estuary MOD V2 Source**: https://github.com/mikesilvo164/skin.estuary.modv2
- **script.skinshortcuts Source**: https://github.com/mikesilvo164/script.skinshortcuts
- **Kodi Python API**: https://codedocs.xyz/xbmc/xbmc/
- **Project Repository**: https://github.com/OutrageousBean/Aurion

## Current Blockers Summary

**PRIMARY BLOCKER**: "Unable to build menu" error from script.skinshortcuts
- **Impact**: 100% - cannot use skin at all
- **Root Cause**: Unknown - needs debug log analysis
- **ETA to Resolve**: Unknown until root cause identified
- **Blocking**: All feature development and testing

**SECONDARY BLOCKER**: No safe way to add custom UI elements
- **Impact**: 60% - major features unusable
- **Root Cause**: Skinshortcuts design incompatible with custom additions
- **ETA to Resolve**: Requires alternative architectural approach
- **Blocking**: Header bar and spotlight features

---

**Last Updated**: November 2, 2025  
**Current Version**: skin.aurion 21.2.1+omega.38  
**Status**: 🔴 BLOCKED - Critical menu build error  
**Next Action**: Enable Kodi debug logging and capture error details
