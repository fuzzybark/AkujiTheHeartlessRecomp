import subprocess
import time
import os

build_dir = r"X:\Dev\psxrecomp\akuji-recomp\AkujiTheHeartlessRecomp\build-release"
exe = os.path.join(build_dir, "AkujiTheHeartless_Recompiled.exe")
settings_path = os.path.join(build_dir, "settings.toml")

cue_path = "X:/Dev/psxrecomp/akuji-recomp/AkujiTheHeartlessRecomp/disc/Akuji the Heartless (USA).cue"

def run_test(name, ir, texfilter, pgxp, fullscreen=0):
    content = f"""[video]
renderer          = "opengl"
window_width      = 1920
window_height     = 1080
stretch_to_fill   = false
geometry_precision= {str(pgxp).lower()}
texture_filtering = {str(texfilter).lower()}
internal_resolution= {ir}
fullscreen        = {fullscreen}

[audio]
master_volume = 0
sfx_volume    = 100
cdda_volume   = 100

[disc]
path = "{cue_path}"
"""
    with open(settings_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n=================== {name} ===================")
    env = os.environ.copy()
    env["PSX_NO_LAUNCHER"] = "1"
    proc = subprocess.Popen([exe, "--no-launcher"],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, cwd=build_dir, env=env)
    time.sleep(2.5)
    proc.terminate()
    try:
        out, err = proc.communicate(timeout=2)
    except Exception:
        proc.kill()
        out, err = proc.communicate()

    lines = (out + "\n" + err).splitlines()
    for l in lines:
        ll = l.lower()
        if any(k in ll for k in ["internal resolution", "pgxp", "texture", "filter", "window", "fullscreen"]):
            print("  LOG:", l)

run_test("Original PS1 Preset (Native 1x, Nearest, PGXP Off)", ir=1, texfilter=False, pgxp=False, fullscreen=0)
run_test("Enhanced PC Preset (1080p, Bilinear, PGXP On)", ir=1080, texfilter=True, pgxp=True, fullscreen=0)
run_test("Windowed Mode (1920x1080 request clamped to usable bounds)", ir=1, texfilter=False, pgxp=False, fullscreen=0)
run_test("Borderless Fullscreen Mode", ir=1, texfilter=False, pgxp=False, fullscreen=1)
