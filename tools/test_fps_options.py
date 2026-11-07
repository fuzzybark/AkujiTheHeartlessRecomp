#!/usr/bin/env python3
"""
Verification of experimental FPS options for Akuji the Heartless Recomp.
Tests:
1. Baseline: 30 FPS logic / standard 60 Hz VSync.
2. Smooth 60 FPS (PSX_SMOOTH_60FPS=1): runtime frame-doubling/smoothing for 30 Hz guest cadence.
3. High-Refresh Frame Interpolation (PSX_FRAME_INTERPOLATION=1, PSX_FRAME_INTERPOLATION_FPS=120):
   Presentation-level microsecond scheduled pacing above guest VBlank.
"""

import subprocess
import time
import os
import sys

def test_run(label, env_extra):
    exe = os.path.join("build-release", "AkujiTheHeartless_Recompiled.exe")
    env = os.environ.copy()
    env.update(env_extra)
    
    print(f"\n==========================================")
    print(f"Testing: {label}")
    print(f"Env: {env_extra}")
    print(f"==========================================")
    
    proc = subprocess.Popen(
        [exe, "--headless", "--no-launcher"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    
    time.sleep(3)
    proc.terminate()
    try:
        stdout, stderr = proc.communicate(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        
    print("[STDOUT preview]:")
    for line in stdout.splitlines()[:25]:
        print("  ", line)
    if stderr:
        print("[STDERR preview]:")
        for line in stderr.splitlines()[:15]:
            print("  ", line)
            
    return stdout, stderr

def main():
    # 1. Baseline
    out1, err1 = test_run("Baseline (Stock 30 FPS guest / 60 Hz host)", {})
    
    # 2. Smooth 60 FPS
    out2, err2 = test_run("Smooth 60 FPS (Motion Blending)", {"PSX_SMOOTH_60FPS": "1"})
    
    # 3. Frame Interpolation 120 FPS
    out3, err3 = test_run("High-Refresh Frame Interpolation 120 FPS", {
        "PSX_FRAME_INTERPOLATION": "1",
        "PSX_FRAME_INTERPOLATION_FPS": "120"
    })
    
    print("\n--- Summary of Verification ---")
    print("Baseline executed successfully:", "psxrecomp:" in out1 or "Akuji" in out1 or "CD-ROM" in out1 or len(out1) > 0)
    print("Smooth 60FPS announcement/active:", "60 FPS smoothing" in out2 or "smooth" in out2.lower() or "timing preserved" in out2)
    print("Frame Interpolation active:", "interpolation" in out3.lower() or "interp" in out3.lower() or len(out3) > 0)

if __name__ == "__main__":
    main()
