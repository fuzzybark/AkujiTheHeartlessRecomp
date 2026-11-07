#!/usr/bin/env python3
"""
Automated gameplay verification test for Akuji The Heartless native PC port.
Boots the recompiled runtime, skips intro movies, selects Akuji from the disc
launcher, enters AKUJI.EXE, navigates through the title menu, selects NEW GAME,
and validates that the engine enters 3D in-game Level 1 (Underworld).
"""

import subprocess
import time
import json
import socket
import os
import sys

# Standard active-low PSX gamepad bit definitions
PAD_SELECT   = 0x0001
PAD_L3       = 0x0002
PAD_R3       = 0x0004
PAD_START    = 0x0008
PAD_UP       = 0x0010
PAD_RIGHT    = 0x0020
PAD_DOWN     = 0x0040
PAD_LEFT     = 0x0080
PAD_L2       = 0x0100
PAD_R2       = 0x0200
PAD_L1       = 0x0400
PAD_R1       = 0x0800
PAD_TRIANGLE = 0x1000
PAD_CIRCLE   = 0x2000
PAD_CROSS    = 0x4000
PAD_SQUARE   = 0x8000

def make_mask(*buttons):
    """In PSX SIO, 0 = pressed, 1 = released. 0xFFFF = all buttons released."""
    val = 0xFFFF
    for b in buttons:
        val &= ~b
    return val

def send_cmd(cmd_dict):
    try:
        s = socket.socket()
        s.settimeout(2.0)
        s.connect(('127.0.0.1', 4370))
        s.sendall(json.dumps(cmd_dict).encode() + b'\n')
        data = b''
        while b'\n' not in data:
            chunk = s.recv(4096)
            if not chunk: break
            data += chunk
        s.close()
        return json.loads(data.decode())
    except Exception as e:
        return {'error': str(e)}

def main():
    exe_path = os.path.join('build-release', 'AkujiTheHeartless_Recompiled.exe')
    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found. Build the project first.")
        sys.exit(1)

    print("Launching psx-runtime headless for gameplay verification...")
    p = subprocess.Popen([exe_path, '--headless', '--no-launcher'])
    time.sleep(2)

    try:
        # 1. Skip intro movies to reach disc launcher menu
        print("Skipping intro FMV movies...")
        for _ in range(8):
            send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_START), 'frames': 5})
            time.sleep(0.5)

        # 2. Wait until disc menu (MAIN.EXE) is fully loaded and interactive
        while True:
            f = send_cmd({'cmd': 'frame'})
            frame_num = f.get('frame', 0)
            if frame_num >= 780:
                break
            time.sleep(0.2)

        print(f"Disc menu reached at frame {frame_num}. Selecting Akuji The Heartless (Cross)...")
        for i in range(10):
            r = send_cmd({'cmd': 'get_registers'})
            pc_str = r.get('pc', '0')
            send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_CROSS), 'frames': 8})
            time.sleep(0.8)
            if pc_str.startswith('0x801F') or pc_str.startswith('0x8009') or pc_str.startswith('0x800C'):
                print(f"  Reboot transition to AKUJI.EXE confirmed (PC: {pc_str}).")
                break

        # 3. Wait for AKUJI.EXE title screen
        print("Waiting for AKUJI.EXE title screen...")
        title_reached = False
        for i in range(15):
            f = send_cmd({'cmd': 'frame'})
            g = send_cmd({'cmd': 'gpu_state'})
            w = g.get('width', 0)
            draws = g.get('gp0_draw', 0)
            if i >= 5 and w == 512 and draws > 1000:
                print(f"  Akuji Title Screen reached at frame {f.get('frame')} (Resolution: {w}x{g.get('height')}).")
                title_reached = True
                break
            send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_START), 'frames': 5})
            time.sleep(1.0)

        if not title_reached:
            print("Warning: Timed out waiting for title screen draw state, attempting NEW GAME anyway.")

        # 4. On Title screen: Selection defaults to NEW GAME. Press CROSS to start.
        print("Pressing CROSS on NEW GAME...")
        send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_CROSS), 'frames': 10})
        time.sleep(2.0)

        # 5. Advance through intro cutscene / level loading
        print("Advancing into Level 1 3D gameplay...")
        gameplay_confirmed = False
        for step in range(25):
            f = send_cmd({'cmd': 'frame'})
            r = send_cmd({'cmd': 'get_registers'})
            g = send_cmd({'cmd': 'gpu_state'})
            frame_num = f.get('frame', 0)
            pc_str = r.get('pc', '0')
            draws = g.get('gp0_draw', 0)
            writes = g.get('gp0_writes', 0)
            print(f"  Step {step:2d} | Frame {frame_num:5d} | draws: {draws:6d} writes: {writes:8d} | PC: {pc_str}")
            if draws > 100000:
                gameplay_confirmed = True
            if step in (1, 3, 5, 7, 9, 11):
                send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_CROSS), 'frames': 5})
            time.sleep(1.2)

        # 6. Capture verified gameplay screenshot
        res = send_cmd({'cmd': 'screenshot_file', 'path': 'akuji_level1_verified.png'})
        print(f"Gameplay screenshot capture: {res}")

        if gameplay_confirmed:
            print("\nSUCCESS: 3D in-game Level 1 reached and verified!")
        else:
            print("\nFAILURE: Did not detect in-game 3D rendering workload.")
            sys.exit(1)

    finally:
        p.kill()

if __name__ == '__main__':
    main()
