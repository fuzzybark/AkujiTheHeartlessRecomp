# Copyright & Licensing Blockers for Public Release

This document analyzes the primary legal questions, copyright blockers, and distribution strategies that must be addressed before publishing **Akuji the Heartless Recomp**.

---

## 1. Primary Legal Blockers

### Blocker 1: Distribution of Statically Recompiled Code (`generated/` and Executable)
* **Underlying Law:** United States Copyright Act (17 U.S.C. &sect; 106) and European Union Computer Programs Directive (2009/24/EC).
* **The Issue:**
  1. The `generated/` directory contains C code produced by mechanically disassembling and decompiling the MIPS object code of *Akuji the Heartless* (`SLUS_007.15`).
  2. The standalone Windows executable (`AkujiTheHeartless_Recompiled.exe`) statically links this translated C code into a 64-bit x86_64 binary.
* **Legal Assessment:**
  - Decompilation and binary translation do not create a new original work of authorship. Under settled copyright law, the resulting C code and compiled binary are legally derivative works of the underlying copyrighted game executable owned by Embracer Group / Crystal Dynamics.
  - While decompilation for *interoperability* is recognized as a lawful exception in some jurisdictions (e.g. 17 U.S.C. &sect; 1201(f) and EU Directive Art. 6), this exception permits reverse engineering to achieve interoperability, **not** public redistribution of the decompiled code itself.
* **Resolution Strategy:**
  - **Open-Source Repository:** The public repository **completely excludes** `generated/`. Contributors and users run `psxrecomp_cli.py generate` on their own legally owned retail game disc locally. This completely avoids distributing copyrighted derivative code in the repository.
  - **Pre-Compiled Binary Distribution:** Distributing `AkujiTheHeartless_Recompiled.exe` publicly remains an **unresolved legal risk** without rights-holder permission. While the package excludes all retail disc assets (textures, music, video), the executable contains translated game logic. Maintainers must treat public binary hosting as legally blocked until authorized.

---

### Blocker 2: PolyForm Noncommercial License 1.0.0 Restrictions
* **Underlying Component:** `psxrecomp` static recompilation framework.
* **The Issue:**
  - `psxrecomp` is licensed under the **PolyForm Noncommercial License 1.0.0**.
  - This license permits personal and community use but strictly forbids any commercial purpose: *"Any use of the software must be for noncommercial purposes only. A purpose is noncommercial if no person receives monetary compensation or anything of value for the use, through sales, subscriptions, advertising, or otherwise."*
* **Resolution Strategy:**
  - No monetization, paywalls, donations gates, or advertising may be attached to the project.
  - All distributed documentation, release archives, and repository notices must include the full PolyForm Noncommercial 1.0.0 license text and preserve upstream author attribution (Matthew Stanley).

---

### Blocker 3: Brand & Trademark Usage
* **Protected Trademarks:** "Akuji", "Akuji the Heartless", and associated game logos are trademarks of Crystal Dynamics / Eidos Interactive / Embracer Group.
* **The Issue:**
  - Using protected game names in a repository name or domain could trigger trademark infringement or false endorsement claims under the Lanham Act (15 U.S.C. &sect; 1125).
* **Resolution Strategy:**
  - Prominently display non-affiliation disclaimers on the website, `README.md`, `README.txt`, and launcher.
  - State clearly: *"This is an unofficial fan project and is not affiliated with, endorsed by, or sponsored by Crystal Dynamics, Eidos Interactive, Embracer Group, or Sony Interactive Entertainment."*
  - Avoid using official corporate logos or trademarks as project branding.

---

## 2. Checklist for Public Authorization

| Item | Status | Action Required |
|---|---|---|
| Exclude `generated/` from public repository | **RESOLVED** | Staged in `publish/source/` with local generation instructions in `generated/README.md`. |
| Exclude retail disc images (`.bin`, `.cue`, `.iso`) | **RESOLVED** | Verified clean across all packages. |
| Exclude Sony retail BIOS images (`SCPH-1001.bin`) | **RESOLVED** | Clean-room OpenBIOS (MIT) bundled exclusively. |
| Exclude memory cards, logs, and crash dumps | **RESOLVED** | Cleaned and filtered via `.gitignore`. |
| Bundle third-party notices and licenses | **RESOLVED** | Bundled in `licenses/` and repository root. |
| Pre-compiled binary distribution clearance | **BLOCKED** | Requires rights-holder approval or formal legal clearance before public hosting. |
| Website deployment to GitHub Pages | **READY** | All pages audited; zero broken links. Ready to deploy when authorized. |
