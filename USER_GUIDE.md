# Akuji the Heartless Recomp — User Guide

This guide covers playing and configuring **Akuji the Heartless Recomp**, including launcher options, graphics presets, display modes, keyboard controls, and presentation frame rates.

---

## 1. Launching the Game

1. Double-click `AkujiTheHeartless_Recompiled.exe` (or run it via command line).
2. The **Recomp Launcher** will open with the following tabs:
   - **Game:** Disc selection, launch button, and quick-setting toggles.
   - **Graphics:** Display mode, window resolution, internal rendering resolution, quality presets, target refresh rate, supersampling, and CRT scanlines.
   - **Audio:** Master volume, sound effects (SFX), and CD-DA redbook audio music levels.
   - **Controller:** Gamepad detection, button mappings, and keyboard keybind configuration.
   - **Mods:** Package management and optional visual/audio extensions.
3. Click **Launch** to start the game.

---

## 2. Graphics Presets & Quality Options

The launcher provides two one-click starting configurations under the **Graphics** tab:

### Original PS1 Preset
* **Internal Resolution:** Native PS1 (1x / 240p)
* **Texture Filtering:** Nearest (crisp, unblurred retro pixels)
* **PGXP Vertex Precision:** Disabled (authentic PS1 polygon jitter)
* **Perspective Texturing:** Disabled (authentic PS1 affine texture warping)
* **CRT Filter:** Disabled
* **Aspect Ratio:** Original 4:3 (pillared on widescreen displays)

### Enhanced PC Preset
* **Internal Resolution:** 1080p, 1440p, or 4K (or match display)
* **Texture Filtering:** Bilinear smoothing
* **PGXP Vertex Precision:** Enabled (eliminates polygon wobbling and seam gaps)
* **Perspective Texturing:** Enabled (perspective-correct texture mapping)
* **CRT Filter:** Optional
* **Aspect Ratio:** Original 4:3 (or Stretch to Fill)

> [!TIP]
> Adjusting any individual setting manually switches the preset label to **Custom**. Reverting settings to match a preset automatically restores the preset label.

---

## 3. Display Modes & Resolutions

* **Display Mode:**
  * `Windowed`: Runs in a movable window matching the selected window resolution.
  * `Borderless Fullscreen`: Fills the monitor seamlessly at native display resolution.
  * `Exclusive Fullscreen`: Binds directly to the display output where supported.
* **Aspect Ratio:**
  * `Original 4:3` (Recommended): Preserves original game geometry proportions with pillarbox bars on widescreen monitors.
  * `Stretch to Fill`: Expands the frame to fill 16:9 or 21:9 monitors.
* **Supported Resolutions:**
  * 4:3: `960×720`, `1280×960`, `1600×1200`, `1920×1440`
  * 16:9: `1280×720`, `1920×1080`, `2560×1440`, `3840×2160`

---

## 4. Target Refresh Rate & Presentation Decoupling

Under the **Graphics** tab, you can set the **Target refresh rate**:

* **Available Rates:**
  * `30 FPS (Original PS1)` — Default authentic PS1 game cadence (interpolation off).
  * `60 FPS` — Smooth presentation pacing at 60 Hz.
  * `120 FPS` — 120 Hz high-refresh pacing.
  * `144 FPS` — 144 Hz high-refresh pacing.
  * `200 FPS` — 200 Hz high-refresh pacing.
  * `240 FPS` — 240 Hz high-refresh pacing.
  * `Match display refresh` — Matches your monitor's native refresh rate (e.g., 144 Hz, 165 Hz, 240 Hz).

> [!NOTE]
> Akuji's gameplay logic and physics execute natively at a fixed 30 Hz tick rate. The recompilation uses **presentation decoupling**: selecting 60, 120, 144, 200, or 240 FPS produces smooth intermediate presentation frames without altering or accelerating game logic, physics, or timers.

### Supersampling (SSAA)
Located under **Graphics** below Internal Resolution:
* `Off (1x)` — Standard internal resolution rendering.
* `2x`, `3x`, `4x` — Renders internally at higher multipliers and downsamples to output, smoothing jagged geometry edges.

---

## 5. Keyboard & Controller Controls

### Default Keyboard Mappings
* **Movement:** Arrow keys (Up, Down, Left, Right)
* **Jump:** Cross (`/` or `Space`)
* **Attack / Claw:** Square (`Z`)
* **Spells / Cast:** Circle (`X`)
* **Action / Interact:** Triangle (`S`)
* **Look / Target:** L1 / R1 (`Q` / `E`)
* **Inventory / Shift:** L2 / R2 (`A` / `D`)
* **Start:** `Enter`
* **Select:** `Shift`

### In-Game Hotkeys
| Key | Action | Function |
|---|---|---|
| **Alt + Enter** | Toggle Fullscreen | Windowed &harr; Borderless Fullscreen |
| **F1** | Quicksave | Saves snapshot to Slot 1 |
| **F3** | Quickload | Restores snapshot from Slot 1 |
| **F5** | Cycle Resolution | Cycles Native &rarr; 720p &rarr; 1080p &rarr; 1440p &rarr; 4K |
| **7** | PGXP Geometry Correction | Toggles sub-pixel vertex precision |
| **8** | Perspective Texturing | Toggles perspective-correct UVs |
| **9** | Texture Filtering | Toggles Bilinear smoothing vs Nearest pixelation |
| **F11** | Toggle CRT Shader | Toggles CRT scanline simulation |
| **Tab** (Hold) | Fast Forward | Speeds up game clock for dialogue/loading |
| **Backspace** | Rewind | Rewinds active gameplay up to 10 seconds |

---

## 6. Save Files & Memory Cards

* Standard PlayStation Memory Card files are maintained in `saves/card1.mcd` and `saves/card2.mcd`.
* In-game save shrines and sanctuary portals save standard save blocks directly into `card1.mcd`.
* Memory cards are compatible with PS1 memory card utilities (such as MemcardRex) for exporting or importing raw `.mcr`/`.mcd` saves.
