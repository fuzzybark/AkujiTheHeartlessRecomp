# Copyright and Third-Party Licensing Audit Report

**Project:** Akuji the Heartless Recomp  
**Baseline Commit:** `5b4e6d6dda78d3320e8b99b5beeb294742643600` (`restore/pre-coop-single-player`)  
**Audit Date:** 2026-11-07  
**Status:** Pre-Publication Legal Assessment  
**Author:** Software Preservation & Licensing Review  

---

## 1. Executive Summary

This comprehensive audit evaluates the intellectual property, copyright, and licensing status of **Akuji the Heartless Recomp** prior to public open-source publication and release distribution.

### Technical Readiness vs. Legal Readiness
> [!IMPORTANT]
> **Technical Readiness &ne; Legal Readiness:**
> While the codebase is technically stable, builds cleanly in Release mode, runs smoothly without crashes, and passes all single-player gameplay verification tests, **legal clearance for public release requires resolving critical intellectual property considerations.**
>
> A strict operational distinction is established between:
> 1. **Open-Source Repository Readiness:** Completely ready when structured as a clean-room workspace (excluding proprietary game code and media).
> 2. **Binary Release Readiness:** Blocked by unresolved copyright questions regarding the distribution of precompiled executables containing translated proprietary machine code.

---

## 2. Component Categorization Matrix

All repository files, dependencies, and artifacts are classified into three distinct categories:

### Category A: Ready for Public Repository Publication (Clean-Room / Permissible)
These components are clean-room, independently authored, or licensed under recognized open-source licenses:

| Component / File Path | Author / Origin | License | Rationale for Publication |
|---|---|---|---|
| **Root CMake Configuration** (`CMakeLists.txt`) | Project Maintainers | MIT License | Clean-room build automation script. |
| **Project Descriptors** (`game.toml`, `game_options.toml`, `VERSION`) | Project Maintainers | MIT License | Configuration descriptors, Redump signatures, and preset definitions. |
| **Input Mappings** (`keybinds.ini`) | Project Maintainers | MIT License | Keyboard and gamepad layout defaults. |
| **Symbol Tables & Seeds** (`symbols.toml`, `seeds/ghidra_funcs.txt`, `psx_symbols.h`) | Reverse Engineering Analysis | Permissive / Functional Information | Non-copyrightable functional interface addresses and decompilation entry point seeds. |
| **AOT Overlay Descriptors** (`aot/overlays.json`) | Project Maintainers | MIT License | Memory boundary layout metadata. |
| **C Adapter Code** (`codegen_setup.c`, `codegen_setup.h`) | Project Maintainers | MIT License | Clean-room C glue code between psxrecomp and launcher. |
| **Diagnostic & Test Suite** (`tools/*.py`) | Project Maintainers | MIT License | Clean-room verification and configuration scripts. |
| **Documentation & Legal** (`*.md`, `publish/documentation/*`, `publish/legal/*`) | Project Maintainers | CC-BY 4.0 / MIT | Documentation, installation instructions, user guides, and legal audits. |
| **Clean Project Assets** (`assets/psxrecomp.*`, `akuji.ico`) | Project / psxrecomp | MIT / Clean Assets | Project iconography and public boxart thumbnail used under nominative fair use. |
| **Mod Framework Skeleton** (`mods/state.toml`, `mods/preloaded/`) | Project Maintainers | MIT License | Empty mod configuration directories. |
| **psxrecomp Submodule** (`psxrecomp/`) | Matthew Stanley | PolyForm Noncommercial 1.0.0 | PS1 static recompilation framework. Upstream open-source project; submodule reference. |
| **recomp-ui Submodule** (`recomp-ui/`) | Matthew Stanley / RetroPortingToolKit | MIT License | ImGui-based standalone launcher. Upstream open-source project; submodule reference. |
| **OpenBIOS** (`psxrecomp/bios/openbios.bin`) | PCSX-Redux authors, Martin Korth, uC-sdk | MIT License | 100% clean-room replacement for Sony PlayStation BIOS. Fully redistributable. |

---

### Category B: Excluded from Publication (and Why)
These files MUST NOT be committed to the public Git repository or uploaded to public mirrors:

| Excluded Component / Pattern | Reason for Exclusion |
|---|---|
| **`generated/` Source Code** (`SLUS_007.15_dispatch.c`, `overlays_static_*.c`, `SLUS_007.15_full_*.c`, `SLUS_007.15_decls.h`) | **Derivative Work of Copyrighted Software:** Directly generated via mechanical MIPS decompilation of the proprietary PlayStation game binary (`SLUS-00715`). Under 17 U.S.C. &sect; 106 and international copyright frameworks, decompiled source code is widely interpreted as an unauthorized derivative work of the underlying software. Excluded to ensure the public repository is a 100% clean-room project. Contributors generate this locally from their own retail disc using `psxrecomp_cli.py`. |
| **Retail Disc Images** (`disc/*.bin`, `disc/*.cue`, `disc/*.iso`, `disc/*.chd`) | **Direct Commercial Game Assets:** Contains copyrighted audio tracks (CD-DA), FMV video cutscenes, level geometry, and texture data owned by Crystal Dynamics / Embracer Group. Unlawful to redistribute under any open-source license. |
| **Sony Retail BIOS ROMs** (`SCPH-1001.bin`, `SCPH-5001.bin`, `SCPH-7001.bin`, etc.) | **Proprietary Firmware:** Copyrighted by Sony Interactive Entertainment LLC. Clean-room OpenBIOS (MIT) is used exclusively instead. |
| **User Save Data & Memory Cards** (`card1.mcd`, `card2.mcd`, `saves/*.mcd`) | **Runtime Artifacts:** Local user gameplay saves, non-code files. |
| **Diagnostic Logs & Traces** (`*.log`, `psx_freeze_dump_*.json`, `probe_run.log`, `crash.log`) | **Ephemeral Scratch Data:** Development artifacts and multi-megabyte freeze dumps. |
| **Compiler Build Artifacts** (`build-release/`, `build-recompiler/`, `.cache/`, `toolchain/`) | **Intermediate Objects:** Machine-specific binary artifacts. |
| **Extraneous Executables** (`tailscale-setup-1.104.4.exe`) | **Unrelated Third-Party Binary:** Must not be committed. |

---

### Category C: Requiring Legal Review or Rights-Holder Permission
These items involve unresolved legal questions that require a management decision or rights-holder clearance:

| Component / Surface | Legal Issue | Current Legal Posture |
|---|---|---|
| **Compiled Windows Executable** (`AkujiTheHeartless_Recompiled.exe`) | Even when packaged without retail disc assets, the binary contains compiled machine code translated from `generated/`. Distributing this binary publicly without rights-holder permission poses copyright risk as an unauthorized derivative work. | **UNRESOLVED BLOCKER:** Technical readiness is complete, but public distribution is legally blocked until authorization is obtained or an explicit fair-use safe harbor is determined. |
| **Trademark Usage** ("Akuji", "Akuji the Heartless") | "Akuji" and "Akuji the Heartless" are trademarks of Crystal Dynamics / Eidos Interactive / Embracer Group. | **CONDITIONAL:** Permissible under nominative fair use provided prominent non-affiliation disclaimers are maintained across all public surfaces and no official logos are used deceptively. |
| **Commercial Exploitation Boundary** (`psxrecomp`) | `psxrecomp` is licensed under PolyForm Noncommercial 1.0.0. | **STRICT NON-COMMERCIAL:** Any commercial use, sales, paid downloads, monetization, or advertising compensation is strictly prohibited. |

---

## 3. Detailed Third-Party Framework & Dependency Audit

Each third-party component has been individually audited. The root repository does not inherit a single overarching license from its dependencies; each component retains its distinct terms:

| Component | Upstream Author / Project | License | Distribution & Attribution Obligations |
|---|---|---|---|
| **Akuji Recomp (Glue / Tools)** | Akuji Recomp Contributors | MIT License | Permissive. Author attribution preserved in source files. |
| **psxrecomp** | Matthew Stanley | PolyForm Noncommercial 1.0.0 | **Non-commercial only.** Commercial distribution, sale, or advertising monetization is strictly forbidden. Attribution must accompany any distribution. |
| **recomp-ui** | Matthew Stanley / RetroPortingToolKit | MIT License | Permissive. Notice and copyright header must accompany binary distributions. |
| **OpenBIOS** | PCSX-Redux authors, Martin Korth, uC-sdk | MIT License | Clean-room replacement BIOS. Permissive; license text packaged alongside `openbios.bin`. |
| **libchdr** | Romain Tisserand & contributors | BSD-3-Clause | CHD decompression library. BSD notice included in `licenses/THIRD_PARTY_LICENSES.md`. |
| **Zstandard** | Meta Platforms, Inc. | BSD-3-Clause / GPL-2.0 | High-performance compression library. BSD notice preserved. |
| **LZMA SDK** | Igor Pavlov | Public Domain | LZMA decompression. |
| **miniz** | Rich Geldreich | MIT License | Deflate/inflate zlib implementation. |
| **SDL3** | Sam Lantinga & contributors | zlib License | Windowing, controller input, and audio backends. |
| **Dear ImGui** | Omar Cornut | MIT License | GUI framework used by recomp-ui launcher. |
| **toml11** | Toru Niina | MIT License | TOML configuration parser. |
| **rabbitizer** | Decompals | MIT License | MIPS instruction lifter and disassembler. |
| **libwebp** | Google Inc. | BSD-3-Clause | WebP image decoder. |

---

## 4. Separation of Publication Readiness

### 4.1 Open-Source Repository Readiness: READY
- The staged directory `publish/source/` contains **only publishable files**.
- All proprietary MIPS translation code (`generated/`) has been replaced by `generated/README.md`, which provides full documentation on generating the C code locally from an authentic retail disc.
- Clean `.gitignore` prevents accidental commits of disc images, BIOS dumps, or translated C code.
- Clean-room submodules (`psxrecomp`, `recomp-ui`) and OpenBIOS are cleanly separated.
- The public open-source repository can be published immediately without copyright infringement.

### 4.2 Windows Binary Release Readiness: TECHNICALLY VERIFIED / LEGALLY BLOCKED
- **Technical Status:** Verified and ready. The archive `akuji-recomp-v0.1.0-windows-x64.zip` (13,599,772 bytes, SHA-256: `B22AFB5B57CA3037CA7E1278B4B82D6C9C166AF8E9ADD2733550917A524A4276`) builds cleanly, includes clean-room OpenBIOS, excludes all disc assets, and launches into stable gameplay.
- **Legal Status:** **UNRESOLVED LEGAL BLOCKER.** Because `AkujiTheHeartless_Recompiled.exe` contains compiled machine code mechanically translated from the copyrighted PlayStation executable, distributing this binary without authorization from Embracer Group / Crystal Dynamics carries copyright liability as a derivative work.
- **Recommended Distribution Strategy:**
  1. Publish the open-source repository as a clean-room compilation workspace.
  2. Direct users and contributors to compile their own binary locally using their retail disc.
  3. Seek written clearance or a community-project safe harbor from the IP holder before offering pre-compiled binary downloads on public mirrors.
