# Installation & Game Files Guide

This guide walks you through acquiring your game disc image, organizing project files, and running **Akuji the Heartless Recomp**.

---

## 1. System Requirements

* **Operating System:** Windows 10 (64-bit, version 1903+) or Windows 11 (64-bit).
* **Processor:** 64-bit x86 dual-core processor (Intel Core i3 / AMD Ryzen 3 or newer).
* **Memory:** 4 GB RAM minimum (8 GB recommended for 4K rendering and supersampling).
* **Graphics:** Dedicated or modern integrated GPU supporting OpenGL 3.3 or higher.
* **Storage:** 150 MB for the executable package + ~700 MB for your CD-ROM disc image.
* **Dependencies:** Microsoft Visual C++ 2015–2022 Redistributable (x64).

---

## 2. Legal Policy on Game Assets

> [!CAUTION]
> **Zero Copyrighted Game Assets Distributed:**
> In compliance with copyright law and software preservation guidelines, Akuji the Heartless Recomp does **not** include any proprietary assets from *Akuji the Heartless*. You must supply your own authentic disc dump. Sharing, requesting, or distributing copyrighted ROMs or disc images on project channels is strictly prohibited.

---

## 3. Supported Game Version

The recompilation was built specifically for the North American (NTSC-U) release:

| Attribute | Value |
|---|---|
| **Game Title** | Akuji the Heartless |
| **Product Serial** | `SLUS-00715` |
| **Region** | North America (NTSC-U) |
| **Format** | CD-ROM (Mode 2 / 2352 bytes/sector) with CD-DA audio tracks |
| **Container** | Redump-compliant `.cue` sheet + multi-track `.bin` files |

---

## 4. Dumping Your Retail CD-ROM

To obtain the required disc image from your original retail PlayStation CD:

1. Insert your original *Akuji the Heartless* disc into your computer's optical disc drive.
2. Launch a reputable disc imaging utility, such as **ImgBurn** or **AnyBurn**.
3. Select **Create image file from disc** (or **Read to Image File**).
4. Set the destination format to **BIN / CUE** (Raw Mode 2).
5. Start the read process.
6. When complete, confirm that your output folder contains:
   - `Akuji the Heartless (USA).cue`
   - `Akuji the Heartless (USA) (Track 1).bin` (Game data track)
   - `Akuji the Heartless (USA) (Track 2).bin` (Audio track)
   - `Akuji the Heartless (USA) (Track 3).bin` (Audio track)

> [!NOTE]
> Single-track `.iso` rips are **not** supported because `.iso` containers strip the redbook CD-DA audio tracks, resulting in silent background music. Multi-track `.bin`/`.cue` images preserve the full game soundtrack.

---

## 5. File Placement & Folder Layout

Extract the release archive and place your `.cue` and `.bin` files inside the `disc/` subdirectory:

```text
AkujiRecomp/
├── AkujiTheHeartless_Recompiled.exe   # Main game executable
├── game.toml                         # Base game configuration
├── game_options.toml                 # Quality presets
├── keybinds.ini                      # Input mappings
├── bios/
│   ├── openbios.bin                  # Clean-room open-source BIOS (MIT)
│   └── OpenBIOS.LICENSE
├── disc/
│   ├── Akuji the Heartless (USA).cue
│   ├── Akuji the Heartless (USA) (Track 1).bin
│   ├── Akuji the Heartless (USA) (Track 2).bin
│   └── Akuji the Heartless (USA) (Track 3).bin
├── mods/
│   └── bundled/                      # Standard framework mod packages
└── saves/                            # Created automatically for memory card saves
```

*Note: You may also store your disc image in any directory and browse to it from the launcher's **Game** tab.*

---

## 6. Running the Game

1. Double-click `AkujiTheHeartless_Recompiled.exe`.
2. The launcher will automatically detect your disc image in `disc/`.
3. Choose your preferred graphics preset (e.g., *Enhanced PC* for 1080p and PGXP precision).
4. Select your target refresh rate under the **Graphics** tab.
5. Click **Launch** to start playing.

---

## 7. Troubleshooting

* **Disc Not Recognized:**
  Open the `.cue` file in a text editor (e.g. Notepad) and ensure the `FILE "..." BINARY` line matches the exact case-sensitive filename of your `.bin` tracks on disk.
* **Controller Not Responding:**
  Ensure your controller is connected before opening the launcher. Switch to the **Controller** tab to verify button mappings.
* **Game Crashes at Startup:**
  Verify that your graphics drivers support OpenGL 3.3 or higher. Check `crash.log` in the game directory if an unexpected termination occurs.
