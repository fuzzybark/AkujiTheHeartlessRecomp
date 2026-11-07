#!/usr/bin/env python3
"""
tools/configure_settings.py - Akuji: The Heartless PC Port Settings Manager

Manages graphics presets, independent visual options, audio volumes, and keyboard profiles.
Presets act as starting baselines and never lock settings.
Custom combinations are detected and reported as 'Custom'.
"""

import sys
import os
import argparse
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODS_STATE_PATH = PROJECT_ROOT / "mods" / "state.toml"
SETTINGS_PATH = PROJECT_ROOT / "settings.toml"
KEYBINDS_PATH = PROJECT_ROOT / "keybinds.ini"
GAME_TOML_PATH = PROJECT_ROOT / "game.toml"

# Presets definitions (starting baselines)
PRESET_ORIGINAL_PS1 = {
    "resolution": "native",
    "texture_filtering": "nearest",
    "pgxp": False,
}

PRESET_ENHANCED_PC = {
    "resolution": "1080p",
    "texture_filtering": "bilinear",
    "pgxp": True,
}

CLASSIC_KEYBINDS = """[player1]
up = Up
down = Down
left = Left
right = Right
cross = X
circle = S
square = Z
triangle = A
l1 = Q
r1 = W
l2 = E
r2 = R
l3 = T
r3 = Y
start = Return
select = Right Shift
ls_up = Up
ls_down = Down
ls_left = Left
ls_right = Right
rs_up = 
rs_down = 
rs_left = 
rs_right = 
"""

MODERN_WASD_KEYBINDS = """[player1]
up = W
down = S
left = A
right = D
cross = Space
circle = L
square = J
triangle = I
l1 = U
r1 = O
l2 = 1
r2 = 2
l3 = G
r3 = H
start = Return
select = Tab
ls_up = W
ls_down = S
ls_left = A
ls_right = D
rs_up = 
rs_down = 
rs_left = 
rs_right = 
"""

def parse_simple_toml(path):
    """Fallback simple parser if tomllib is unavailable."""
    if not path.exists():
        return {}
    if tomllib:
        with open(path, "rb") as f:
            return tomllib.load(f)
    # Basic fallback
    res = {}
    current_sec = res
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                sec_name = line[1:-1].strip()
                res[sec_name] = {}
                current_sec = res[sec_name]
            elif "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                current_sec[k] = v
    return res

def get_current_graphics_state():
    state = {
        "resolution": "native",
        "texture_filtering": "nearest",
        "pgxp": False,
    }
    if not MODS_STATE_PATH.exists():
        return state

    try:
        data = parse_simple_toml(MODS_STATE_PATH)
        # Check modern [[feature]] list first
        features = data.get("feature", [])
        if isinstance(features, list) and len(features) > 0:
            for feat in features:
                pkg_id = feat.get("package_id", "")
                enabled = feat.get("enabled", False)
                values = feat.get("values", {})
                if pkg_id == "psx.enhancement.internal-resolution":
                    if enabled:
                        state["resolution"] = values.get("resolution", "native")
                    else:
                        state["resolution"] = "native"
                elif pkg_id == "psx.enhancement.image-filtering":
                    if enabled:
                        state["texture_filtering"] = values.get("texture_filtering", "nearest")
                    else:
                        state["texture_filtering"] = "nearest"
                elif pkg_id == "psx.enhancement.pgxp":
                    state["pgxp"] = bool(enabled)
            return state

        # Fallback to legacy [[package]] list
        packages = data.get("package", [])
        if isinstance(packages, list):
            for pkg in packages:
                pkg_id = pkg.get("id", "")
                enabled = pkg.get("enabled", False)
                values = pkg.get("values", {})
                if pkg_id == "psx.enhancement.internal-resolution":
                    if enabled:
                        state["resolution"] = values.get("resolution", "native")
                    else:
                        state["resolution"] = "native"
                elif pkg_id == "psx.enhancement.image-filtering":
                    if enabled:
                        state["texture_filtering"] = values.get("texture_filtering", "nearest")
                    else:
                        state["texture_filtering"] = "nearest"
                elif pkg_id == "psx.enhancement.pgxp":
                    state["pgxp"] = bool(enabled)
    except Exception as e:
        print(f"[warning] failed parsing {MODS_STATE_PATH}: {e}", file=sys.stderr)
    return state

def get_current_settings():
    s = {
        "fullscreen": 0,
        "vsync": "on",
        "master_volume": 100,
        "sfx_volume": 100,
        "cdda_volume": 100,
        "buffer_ms": 40,
    }
    if not SETTINGS_PATH.exists():
        return s
    try:
        data = parse_simple_toml(SETTINGS_PATH)
        video = data.get("video", {})
        audio = data.get("audio", {})
        if "fullscreen" in video:
            try: s["fullscreen"] = int(video["fullscreen"])
            except: pass
        if "vsync" in video:
            s["vsync"] = str(video["vsync"]).strip('"')
        if "master_volume" in audio:
            try: s["master_volume"] = int(audio["master_volume"])
            except: pass
        if "sfx_volume" in audio:
            try: s["sfx_volume"] = int(audio["sfx_volume"])
            except: pass
        if "cdda_volume" in audio:
            try: s["cdda_volume"] = int(audio["cdda_volume"])
            except: pass
        if "buffer_ms" in audio:
            try: s["buffer_ms"] = int(audio["buffer_ms"])
            except: pass
    except Exception as e:
        print(f"[warning] failed parsing {SETTINGS_PATH}: {e}", file=sys.stderr)
    return s

def get_current_keybind_profile():
    if not KEYBINDS_PATH.exists():
        return "classic"
    try:
        content = KEYBINDS_PATH.read_text(encoding="utf-8")
        if "up = W" in content or "up = w" in content:
            return "modern_wasd"
        return "classic"
    except:
        return "classic"

def identify_preset(gfx):
    if (gfx["resolution"] == PRESET_ORIGINAL_PS1["resolution"] and
        gfx["texture_filtering"] == PRESET_ORIGINAL_PS1["texture_filtering"] and
        gfx["pgxp"] == PRESET_ORIGINAL_PS1["pgxp"]):
        return "Original PS1"
    if (gfx["resolution"] in ("1080p", "1440p", "4k") and
        gfx["texture_filtering"] == PRESET_ENHANCED_PC["texture_filtering"] and
        gfx["pgxp"] == PRESET_ENHANCED_PC["pgxp"]):
        if gfx["resolution"] == "1080p":
            return "Enhanced PC"
        else:
            return f"Enhanced PC ({gfx['resolution'].upper()})"
    return "Custom"

def save_mods_state(gfx):
    res_enabled = gfx["resolution"] != "native"
    filt_enabled = gfx["texture_filtering"] != "nearest"
    pgxp_enabled = bool(gfx["pgxp"])

    lines = [
        "# psxrecomp user mod state - generated by configure_settings.py",
        "format_version = 2\n",
        "[[package]]",
        'id = "psx.enhancement.internal-resolution"',
        'version = "1.0.0"\n',
        "[[package]]",
        'id = "psx.enhancement.image-filtering"',
        'version = "1.0.0"\n',
        "[[package]]",
        'id = "psx.enhancement.pgxp"',
        'version = "1.0.0"\n',
        "[[package]]",
        'id = "psx.enhancement.crt-filter"',
        'version = "1.0.0"\n',
        "[[feature]]",
        'package_id = "psx.enhancement.internal-resolution"',
        'id = "internal-resolution"',
        f"enabled = {'true' if res_enabled else 'false'}",
        "[feature.values]",
        f'resolution = "{gfx["resolution"]}"\n',
        "[[feature]]",
        'package_id = "psx.enhancement.image-filtering"',
        'id = "image-filtering"',
        f"enabled = {'true' if filt_enabled else 'false'}",
        "[feature.values]",
        f'texture_filtering = "{gfx["texture_filtering"]}"\n',
        "[[feature]]",
        'package_id = "psx.enhancement.pgxp"',
        'id = "pgxp"',
        f"enabled = {'true' if pgxp_enabled else 'false'}\n",
        "[[feature]]",
        'package_id = "psx.enhancement.crt-filter"',
        'id = "crt-filter"',
        "enabled = false\n",
    ]
    content = "\n".join(lines) + "\n"
    targets = [MODS_STATE_PATH]
    build_release_state = PROJECT_ROOT / "build-release" / "mods" / "state.toml"
    if build_release_state.parent.exists():
        targets.append(build_release_state)
    for p in targets:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

def save_settings(settings):
    lines = [
        "# psxrecomp user settings - written by configure_settings.py",
        "# Safe to hand-edit or update via tools/configure_settings.py\n",
        "[video]",
        f'fullscreen = {settings["fullscreen"]}',
        f'vsync      = "{settings["vsync"]}"\n',
        "[audio]",
        f'master_volume = {settings["master_volume"]}',
        f'sfx_volume    = {settings["sfx_volume"]}',
        f'cdda_volume   = {settings["cdda_volume"]}',
        f'buffer_ms     = {settings["buffer_ms"]}\n',
    ]
    content = "\n".join(lines) + "\n"
    targets = [SETTINGS_PATH]
    build_release_settings = PROJECT_ROOT / "build-release" / "settings.toml"
    if (PROJECT_ROOT / "build-release").exists():
        targets.append(build_release_settings)
    for p in targets:
        p.write_text(content, encoding="utf-8")

def save_keybinds(profile):
    content = MODERN_WASD_KEYBINDS if profile == "modern_wasd" else CLASSIC_KEYBINDS
    targets = [KEYBINDS_PATH]
    build_release_keybinds = PROJECT_ROOT / "build-release" / "keybinds.ini"
    if (PROJECT_ROOT / "build-release").exists():
        targets.append(build_release_keybinds)
    for p in targets:
        p.write_text(content, encoding="utf-8")

def print_status():
    gfx = get_current_graphics_state()
    s = get_current_settings()
    k = get_current_keybind_profile()
    preset = identify_preset(gfx)

    fs_names = {0: "Windowed", 1: "Borderless Desktop", 2: "Exclusive Fullscreen"}
    fs_str = fs_names.get(s["fullscreen"], f"Unknown ({s['fullscreen']})")

    print("============================================================")
    print("      AKUJI: THE HEARTLESS RECOMP - PC CONFIGURATION        ")
    print("============================================================")
    print(f" Active Graphics Preset:  {preset}")
    print(" -----------------------------------------------------------")
    print(f"   Internal Resolution:   {gfx['resolution']}")
    print(f"   Texture Filtering:     {gfx['texture_filtering']}")
    print(f"   PGXP Precision:        {'Enabled' if gfx['pgxp'] else 'Disabled'}")
    print(f"   CRT Effects:           Disabled")
    print(" -----------------------------------------------------------")
    print(f"   Display Mode:          {fs_str}")
    print(f"   VSync:                 {s['vsync']}")
    print(" -----------------------------------------------------------")
    print(f"   Master Volume:         {s['master_volume']}%")
    print(f"   SPU SFX Volume:        {s['sfx_volume']}%")
    print(f"   CDDA Music Volume:     {s['cdda_volume']}%")
    print(f"   Audio Buffer Cushion:  {s['buffer_ms']} ms")
    print(" -----------------------------------------------------------")
    print(f"   Keyboard Profile:      {k} ({'Arrow keys' if k == 'classic' else 'WASD + Space/J/L/I'})")
    print("============================================================")

def main():
    parser = argparse.ArgumentParser(description="Configure Akuji: The Heartless PC Port Settings")
    parser.add_argument("--status", action="store_true", help="Display current configuration and active preset")
    parser.add_argument("--preset", choices=["original", "enhanced", "enhanced_1440p", "enhanced_4k"],
                        help="Apply starting baseline preset: 'original' (PS1 1x native) or 'enhanced' (PC 1080p)")
    # Independent graphics overrides
    parser.add_argument("--resolution", choices=["native", "720p", "1080p", "1440p", "4k"],
                        help="Set internal rendering resolution independently")
    parser.add_argument("--texture-filtering", choices=["nearest", "bilinear"],
                        help="Set texture filtering independently")
    parser.add_argument("--pgxp", choices=["on", "off"],
                        help="Enable or disable PGXP sub-pixel geometry correction independently")
    # Display overrides
    parser.add_argument("--fullscreen", choices=["0", "1", "2", "windowed", "borderless", "exclusive"],
                        help="Set fullscreen mode (0=windowed, 1=borderless, 2=exclusive)")
    parser.add_argument("--vsync", choices=["on", "immediate", "adaptive", "vrr"],
                        help="Set VSync mode")
    # Audio overrides
    parser.add_argument("--master-volume", type=int, choices=range(0, 101), metavar="0..100",
                        help="Set Master Volume (0-100%%)")
    parser.add_argument("--sfx-volume", type=int, choices=range(0, 101), metavar="0..100",
                        help="Set SPU Sound Effects Volume (0-100%%)")
    parser.add_argument("--music-volume", type=int, choices=range(0, 101), metavar="0..100",
                        help="Set CDDA Disc Music Volume (0-100%%)")
    parser.add_argument("--buffer-ms", type=int, metavar="30..500",
                        help="Set audio cushion latency in ms (default 40 ms)")
    # Input profile
    parser.add_argument("--keybinds", choices=["classic", "modern_wasd"],
                        help="Select keyboard binding profile (classic arrows or modern WASD)")

    args = parser.parse_args()

    gfx = get_current_graphics_state()
    settings = get_current_settings()
    keybind_profile = get_current_keybind_profile()

    modified = False

    # Apply preset if requested
    if args.preset == "original":
        gfx.update(PRESET_ORIGINAL_PS1)
        modified = True
    elif args.preset == "enhanced":
        gfx.update(PRESET_ENHANCED_PC)
        modified = True
    elif args.preset == "enhanced_1440p":
        gfx.update(PRESET_ENHANCED_PC)
        gfx["resolution"] = "1440p"
        modified = True
    elif args.preset == "enhanced_4k":
        gfx.update(PRESET_ENHANCED_PC)
        gfx["resolution"] = "4k"
        modified = True

    # Apply independent graphics overrides
    if args.resolution:
        gfx["resolution"] = args.resolution
        modified = True
    if args.texture_filtering:
        gfx["texture_filtering"] = args.texture_filtering
        modified = True
    if args.pgxp:
        gfx["pgxp"] = (args.pgxp == "on")
        modified = True

    # Apply display overrides
    if args.fullscreen:
        mapping = {"0": 0, "windowed": 0, "1": 1, "borderless": 1, "2": 2, "exclusive": 2}
        settings["fullscreen"] = mapping[args.fullscreen]
        modified = True
    if args.vsync:
        settings["vsync"] = args.vsync
        modified = True

    # Apply audio overrides
    if args.master_volume is not None:
        settings["master_volume"] = max(0, min(100, args.master_volume))
        modified = True
    if args.sfx_volume is not None:
        settings["sfx_volume"] = max(0, min(100, args.sfx_volume))
        modified = True
    if args.music_volume is not None:
        settings["cdda_volume"] = max(0, min(100, args.music_volume))
        modified = True
    if args.buffer_ms is not None:
        settings["buffer_ms"] = max(30, min(500, args.buffer_ms))
        modified = True

    # Apply keybinds
    if args.keybinds:
        keybind_profile = args.keybinds
        save_keybinds(keybind_profile)
        modified = True

    if modified:
        save_mods_state(gfx)
        save_settings(settings)
        print("[success] Configuration updated successfully.")

    print_status()

if __name__ == "__main__":
    main()
