# Aurion AI Development Guide

This guide helps AI agents understand and work effectively with the Aurion Kodi addon project.

## Project Overview

Aurion consists of two main components:
- `plugin.video.aurion`: A Kodi video plugin addon
- `skin.aurion`: A custom Kodi skin theme

## Architecture & Structure

### Skin Component (`skin.aurion/`)
- `xml/`: Contains UI definition files in XML format
- `media/`: Theme assets and textures (`.xbt` files)
- `colors/`: Color scheme definitions for different themes
- `shortcuts/`: Menu and shortcut configurations
- `scripts/`: Python helper scripts for context menus and services
- `language/`: Internationalization resources for multiple languages

### Video Plugin (`plugin.video.aurion/`)
- Main functionality implemented in `main.py`
- Uses standard Kodi addon structure and APIs

## Key Development Workflows

### Building
- Use `tools/build.py` for packaging addons into installable zip files
- Built packages are placed in the `zips/` directory

### Theme Development
1. Modify XML files in `skin.aurion/xml/` for UI layouts
2. Define colors in `skin.aurion/colors/` XMLs
3. Add assets to `skin.aurion/media/`
4. Update language strings in `skin.aurion/language/` as needed

### Plugin Development
- Follow Kodi plugin development guidelines
- Use helper scripts in `skin.aurion/scripts/` for UI integration

## Project-Specific Patterns

### Skin Customization
- Color schemes are defined in XML files under `colors/`
- Multiple themes supported: "curial" and "flat" (`themes/` directory)
- Custom views configured in `extras/views.xml`

### Menu System
- Shortcuts defined in `shortcuts/*.DATA.xml`
- Override behavior configured in `shortcuts/overrides.xml`
- Template system using `shortcuts/template.xml`

### Internationalization
- Language resources organized by locale in `language/resource.language.*`
- Follow existing string ID patterns when adding new text

## Integration Points

### Plugin-Skin Integration
- Video plugin integrates with skin through Kodi's addon API
- Context menus defined in `scripts/context_menu_*.py`
- Service scripts in `scripts/services.py` handle background tasks

## Common Tasks

1. Adding a new color theme:
   - Create new XML in `skin.aurion/colors/`
   - Follow pattern of existing files like `brown.xml`, `charcoal.xml`

2. Creating a new menu shortcut:
   - Add definition to appropriate `shortcuts/*.DATA.xml`
   - Update overrides if needed in `overrides.xml`

3. Adding language support:
   - Create new locale directory under `language/`
   - Copy string definitions from existing locale as template

## Best Practices

1. Keep XML UI definitions modular and reusable
2. Follow existing naming conventions for colors and views
3. Maintain language strings for all user-facing text
4. Use helper scripts for complex UI interactions
5. Test changes with different color schemes and themes