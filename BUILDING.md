# Building Akuji Recomp from Source

This document outlines the prerequisites, clean-room architecture, and compilation process for building **Akuji the Heartless Recomp** on Windows 64-bit.

---

## 1. Prerequisites

Ensure the following tools are installed and accessible in your system `PATH`:

1. **Git:** [git-scm.com](https://git-scm.com)
2. **CMake:** Version 3.25 or newer ([cmake.org](https://cmake.org/download/))
3. **Clang / LLVM:** LLVM 16+ or Clang toolchain ([llvm.org](https://github.com/llvm/llvm-project/releases))
4. **Ninja:** Fast build system ([ninja-build.org](https://ninja-build.org/))
5. **Python:** Version 3.10 or newer ([python.org](https://python.org))

---

## 2. Cloning the Repository

Clone the repository and recursively initialize all clean-room submodules (`psxrecomp`, `recomp-ui`):

```bash
git clone https://github.com/<organization>/AkujiTheHeartlessRecomp.git
cd AkujiTheHeartlessRecomp
git submodule update --init --recursive
```

---

## 3. Clean-Room Repository Architecture

To maintain complete legal compliance with copyright law, this public repository contains **zero** commercial game assets, zero proprietary Sony BIOS dumps, and **zero** mechanically translated game code:

* `CMakeLists.txt`: Root build configuration linking the generated game runtime with psxrecomp and recomp-ui.
* `psxrecomp/`: Submodule containing the PlayStation static recompilation framework, peripheral simulation (GPU, SPU, CD-ROM, DMA), and OpenBIOS integration (PolyForm Noncommercial 1.0.0).
* `recomp-ui/`: Submodule providing the ImGui-based standalone launcher, settings persistence, and gamepad mapper (MIT).
* `game.toml` & `game_options.toml`: Configuration descriptors defining Redump signatures, memory maps, and quality presets.
* `seeds/ghidra_funcs.txt`: Symbolic function entry seeds for static decompilation.
* `aot/overlays.json`: Memory boundary specifications for overlay loading.
* `generated/`: **Excluded from repository.** Contributors emit this directory locally from their own legally owned retail disc.

---

## 4. Generating the Game C Locally

Before compiling the runtime, generate the native C source files from your retail PlayStation disc:

1. Obtain a clean Redump-verified CUE/BIN disc image of **Akuji the Heartless (USA)** (`SLUS-00715`).
2. Place the disc files in the `disc/` directory:
   - `disc/Akuji the Heartless (USA).cue`
   - `disc/Akuji the Heartless (USA) (Track 1).bin`
   - `disc/Akuji the Heartless (USA) (Track 2).bin`
   - `disc/Akuji the Heartless (USA) (Track 3).bin`
3. Run the static recompiler CLI:
   ```bash
   python psxrecomp/psxrecomp_cli.py generate \
     --config game.toml \
     --project-root . \
     --disc "disc/Akuji the Heartless (USA).cue"
   ```
4. This emits the translated C source files into `generated/`:
   - `generated/SLUS_007.15_dispatch.c`
   - `generated/SLUS_007.15_full_00.c`
   - `generated/SLUS_007.15_full_01.c`
   - `generated/overlays_static.c`
   - `generated/overlays_static_*.c`

---

## 5. Compiling the Release Binary

Once `generated/` has been emitted, configure and compile the project using CMake and Ninja:

```bash
# 1. Create and configure build directory in Release mode
cmake -S . -B build-release -G Ninja -DCMAKE_BUILD_TYPE=Release

# 2. Build the recompiled game runtime
cmake --build build-release --config Release
```

Upon successful compilation, the executable will be produced at:
`build-release/AkujiTheHeartless_Recompiled.exe`

---

## 6. Running and Verifying

1. Double-click `build-release/AkujiTheHeartless_Recompiled.exe`.
2. The launcher will automatically detect your disc image in `disc/`.
3. Choose your desired graphics preset (*Enhanced PC* recommended for 1080p / 60+ FPS).
4. Click **Launch** to play.
