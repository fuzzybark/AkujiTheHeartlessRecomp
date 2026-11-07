# Local Game Code Generation (generated/)

## Why is this directory empty in the public repository?

Under United States copyright law (17 U.S.C. § 106) and international copyright conventions, mechanically translating or decompiling commercial machine code into native C source code creates a derivative work of the original software.

Because **Akuji the Heartless** is copyrighted by Crystal Dynamics / Eidos Interactive / Embracer Group, distributing pre-generated C translation files (`SLUS_007.15_dispatch.c`, `overlays_static_*.c`, etc.) in a public repository carries legal copyright liability.

To keep this project 100% clean-room and legally sound for open-source collaboration, **no translated game C code is committed to this repository**.

---

## How to Generate the Game C Locally

As a contributor or player compiling from source, you generate these files locally on your own computer using your legally owned retail copy of the game disc.

### Step 1: Dump your Retail CD-ROM
Obtain a clean Redump-verified CUE/BIN disc image of **Akuji the Heartless (USA)** (`SLUS-00715`).
Place the disc image files inside the `disc/` directory:
- `disc/Akuji the Heartless (USA).cue`
- `disc/Akuji the Heartless (USA) (Track 1).bin`
- `disc/Akuji the Heartless (USA) (Track 2).bin`
- `disc/Akuji the Heartless (USA) (Track 3).bin`

### Step 2: Run the psxrecomp Static Recompiler CLI
Execute the static recompiler CLI from the project root:

```bash
python psxrecomp/psxrecomp_cli.py generate \
  --config game.toml \
  --project-root . \
  --disc "disc/Akuji the Heartless (USA).cue"
```

This automated step:
1. Verifies your disc image hashes against `game.toml` Redump signatures.
2. Extracts the `SLUS_007.15` PlayStation executable.
3. Disassembles and lifts MIPS instructions using `seeds/ghidra_funcs.txt`.
4. Emits native C translation files directly into this `generated/` directory:
   - `generated/SLUS_007.15_dispatch.c`
   - `generated/SLUS_007.15_full_00.c`
   - `generated/SLUS_007.15_full_01.c`
   - `generated/overlays_static.c`
   - `generated/overlays_static_0000.c` .. `0003.c`
   - `generated/SLUS_007.15_decls.h`
   - `generated/AOT_STATIC_AUDIT.json`

### Step 3: Build the Project
Once the `generated/` files are present, proceed with standard CMake compilation:

```bash
cmake -S . -B build-release -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build-release --config Release
```

For more details, see [`BUILDING.md`](../BUILDING.md).
