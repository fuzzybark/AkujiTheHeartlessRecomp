# Akuji the Heartless Recompiled

[![Release](https://img.shields.io/badge/Release-v0.1.0-red.svg)](https://github.com/<organization>/AkujiTheHeartlessRecomp/releases)
[![Platform](https://img.shields.io/badge/Platform-Windows%20x64-blue.svg)](https://github.com/<organization>/AkujiTheHeartlessRecomp)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Engine: PolyForm Noncommercial](https://img.shields.io/badge/Engine-PolyForm%20Noncommercial-orange.svg)](https://polyformproject.org/licenses/noncommercial/1.0.0)

A native 64-bit Windows static recompilation project for the 1998 PlayStation classic **Akuji the Heartless** (*SLUS-00715*), built on the [psxrecomp](https://github.com/mstan/psxrecomp) runtime and [recomp-ui](https://github.com/RetroPortingToolKit/recomp-ui) launcher.

---

## Overview

Unlike emulators that interpret or dynamically recompile MIPS instructions at runtime, static recompilation translates PlayStation binaries ahead of time into native C code. When compiled for modern 64-bit platforms, the game executes natively with zero emulation overhead, instant load times, and modern PC enhancements.

> [!NOTE]
> This static recompilation was tested and verified with the **SLUS-00715** version of the game (**USA**, NTSC-U). Ensure your disc dump matches the USA retail release in multi-track CUE/BIN format.

### Key Enhancements

* **Arbitrary High-Resolution Rendering:** Internal rendering up to 4K+ UHD with windowed, borderless, and exclusive fullscreen modes.
* **PGXP Sub-Pixel Precision:** Eliminates characteristic PlayStation 3D polygon jitter, vertex wobble, and polygon seam tearing.
* **Perspective-Correct Texturing:** Corrects affine UV interpolation on 3D geometry.
* **Presentation Decoupling:** Smooth frame presentation pacing at 60, 120, 144, 200, 240 FPS or monitor refresh sync without altering the fixed 30 Hz game physics.
* **Supersampling (SSAA):** Internal supersampling up to 4x for ultra-sharp polygon anti-aliasing.
* **Clean-Room OpenBIOS:** Bundled with open-source OpenBIOS (MIT). No proprietary Sony retail BIOS dump is required.
* **Controller & Keyboard Support:** Full native support for Xbox (XInput), PlayStation (DualShock 4 / DualSense), Switch Pro, and DirectInput controllers, plus customizable keyboard mappings.
* **Save State & Rewind Support:** Instantaneous quicksaves (`F1`/`F3`) and 10-second real-time gameplay rewind (`Backspace`).
* **Standard Memory Cards:** Full compatibility with standard `.mcd` memory card files in `saves/card1.mcd`.

---

## Clean-Room Legal Architecture

> [!IMPORTANT]
> **Zero Copyrighted Assets Distributed:**
> In strict compliance with copyright law and clean-room development principles, this repository distributes **zero** commercial game assets, level data, textures, audio tracks, models, or proprietary BIOS ROMs.
>
> Furthermore, **mechanically translated game code (`generated/`) is excluded from this repository** to avoid copyright liability as an unauthorized derivative work. Contributors and players generate the game C locally from their own legally owned retail copy of the game disc (`SLUS-00715`) using the provided static recompiler toolchain.

---

## Getting Started

### For Contributors & Builders
1. Clone this repository with submodules:
   ```bash
   git clone https://github.com/<organization>/AkujiTheHeartlessRecomp.git --recursive
   ```
2. Place your legally dumped `Akuji the Heartless (USA).cue` and `.bin` tracks into `disc/`.
3. Generate the local game C:
   ```bash
   python psxrecomp/psxrecomp_cli.py generate --config game.toml --project-root . --disc "disc/Akuji the Heartless (USA).cue"
   ```
4. Build the Release binary:
   ```bash
   cmake -S . -B build-release -G Ninja -DCMAKE_BUILD_TYPE=Release
   cmake --build build-release --config Release
   ```
5. See [BUILDING.md](BUILDING.md) for full instructions.

### For Players (Windows x64 Release Package)
1. Download `akuji-recomp-v0.1.0-windows-x64.zip` from the project release page.
2. Extract the archive into a folder on your computer.
3. Place your legally dumped `Akuji the Heartless (USA).cue` and `.bin` files into the `disc/` folder (or select them via the launcher).
4. Run `AkujiTheHeartless_Recompiled.exe`.
5. Select your preferred display preset and click **Launch**.
6. See [INSTALLATION.md](INSTALLATION.md) for disc dumping and configuration steps.

---

## Documentation Index

* [**Building from Source**](BUILDING.md): Toolchain setup, local C generation, and compilation instructions.
* [**Installation Guide**](INSTALLATION.md): How to dump your disc and configure game files.
* [**User Guide**](USER_GUIDE.md): Graphics presets, display options, keyboard shortcuts, and gamepad bindings.
* [**Contributing Guidelines**](CONTRIBUTING.md): Clean-room rules, issue workflow, and pull request guidelines.
* [**Security Policy**](SECURITY.md): Vulnerability reporting procedures.
* [**Copyright & License Audit**](AUDIT_REPORT.md): In-depth legal analysis of code, assets, and frameworks.
* [**Copyright Blockers Analysis**](COPYRIGHT_BLOCKERS.md): Detailed assessment of open-source vs. binary distribution legal blockers.
* [**Third-Party Licenses**](THIRD_PARTY_LICENSES.md): Full license texts for all upstream dependencies.

---

## Licensing & Disclaimers

* **Repository Adapter Code:** Licensed under the [MIT License](LICENSE).
* **psxrecomp Engine:** Licensed under the [PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0). Commercial use is strictly prohibited.
* **recomp-ui Launcher:** Licensed under the [MIT License](https://opensource.org/licenses/MIT).
* **OpenBIOS:** Licensed under the [MIT License](https://opensource.org/licenses/MIT).

*Akuji the Heartless* is &copy; 1998 Crystal Dynamics / Eidos Interactive / Embracer Group. This fan-made project is not affiliated with, endorsed by, or sponsored by Crystal Dynamics, Eidos Interactive, Embracer Group, or Sony Interactive Entertainment.

---

*This project was developed with assistance from Google's Gemini AI models, the project is maintained as an open-source community effort, and contributions from other developers are welcome.*
