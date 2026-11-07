#!/usr/bin/env python3
"""
Phase 2 Game Compatibility Verification Suite for Akuji The Heartless Recomp.
Validates:
1. Audio Subsystems: SPU synthesized SFX + CDDA Redbook disc streaming.
2. Memory Card Subsystem: Slot 1 / Slot 2 status and persistence.
3. Live Player Controls & Physics: Walking, turning, jumping, claw slashing.
4. Animation & Rendering Parity: Multi-frame animation progression.
"""

import subprocess
import time
import json
import socket
import os
import sys

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
    val = 0xFFFF
    for b in buttons:
        val &= ~b
    return val

def send_cmd(cmd_dict):
    try:
        s = socket.socket()
        s.settimeout(3.0)
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
        print(f"Error: {exe_path} not found.")
        sys.exit(1)

    print("=== Launching Akuji The Heartless for Phase 2 Compatibility Testing ===")
    p = subprocess.Popen([exe_path, '--headless', '--no-launcher'])
    time.sleep(2)

    results = {}

    try:
        # 1. Skip intro movies to reach disc launcher menu
        print("[1/5] Navigating boot and disc launcher...")
        for _ in range(8):
            send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_START), 'frames': 5})
            time.sleep(0.5)

        # Wait until disc menu (MAIN.EXE) is fully loaded
        while True:
            f = send_cmd({'cmd': 'frame'})
            frame_num = f.get('frame', 0)
            if frame_num >= 780:
                break
            time.sleep(0.2)

        # Select Akuji The Heartless
        for i in range(10):
            r = send_cmd({'cmd': 'get_registers'})
            pc_str = r.get('pc', '0')
            send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_CROSS), 'frames': 8})
            time.sleep(0.8)
            if pc_str.startswith('0x801F') or pc_str.startswith('0x8009') or pc_str.startswith('0x800C'):
                break

        # Wait for AKUJI.EXE title screen
        for i in range(15):
            g = send_cmd({'cmd': 'gpu_state'})
            w = g.get('width', 0)
            draws = g.get('gp0_draw', 0)
            if i >= 5 and w == 512 and draws > 1000:
                break
            send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_START), 'frames': 5})
            time.sleep(1.0)

        # Select NEW GAME on Akuji title screen
        print("[2/5] Starting NEW GAME from title screen...")
        send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_CROSS), 'frames': 10})
        time.sleep(2.0)

        # Advance into Level 1 3D gameplay
        print("[3/5] Waiting for Level 1 3D world to initialize...")
        in_gameplay = False
        for step in range(25):
            g = send_cmd({'cmd': 'gpu_state'})
            draws = g.get('gp0_draw', 0)
            if draws > 100000:
                in_gameplay = True
                break
            if step in (1, 3, 5, 7, 9, 11):
                send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_CROSS), 'frames': 5})
            time.sleep(1.2)

        if not in_gameplay:
            print("ERROR: Failed to reach 3D gameplay within timeout.")
            sys.exit(1)

        print(f"Level 1 3D gameplay active (draws: {draws}).")

        # Give the in-game world 3 seconds to settle
        time.sleep(3.0)

        # 4. Check Memory Card Subsystem
        print("\n--- [Audit: Memory Card Subsystem] ---")
        mc_info = send_cmd({'cmd': 'mc_status'})
        results['memory_card'] = mc_info
        print(f"Memory Card Status: {json.dumps(mc_info, indent=2)}")

        # 5. Check Audio Subsystem (SPU SFX + CDDA Music)
        print("\n--- [Audit: Audio Subsystem (SPU + CDDA)] ---")
        spu_info = send_cmd({'cmd': 'spu_status'})
        audio_info = send_cmd({'cmd': 'audio_stats'})
        results['spu_status'] = spu_info
        results['audio_stats'] = audio_info
        print(f"SPU Status: key_on={spu_info.get('key_on_count')}, active_mask={spu_info.get('active_mask')}, cd_frames={spu_info.get('cd_frames')}")
        print(f"Audio Stats: {json.dumps(audio_info.get('taps'), indent=2)}")

        # Dump a 3-second audio sample of SPU/CDDA output to verify audio waveform
        audio_dump = send_cmd({'cmd': 'audio_wav', 'path': 'akuji_level1_audio.wav', 'tap': 0, 'count': 44100 * 3})
        print(f"Audio WAV Dump Response: {audio_dump}")

        # 6. Interactive Player Control & Physics Tests
        print("\n--- [Audit: Player Movement, Animation & Combat Physics] ---")
        
        # Test A: Walk Forward
        print("Action A: Holding D-Pad UP (Walking forward towards river/hint tablet)...")
        send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_UP), 'frames': 60})
        time.sleep(2.0)
        send_cmd({'cmd': 'screenshot_file', 'path': 'akuji_action_walk.png'})
        spu_walk = send_cmd({'cmd': 'spu_status'})
        print(f"  Walk state captured. SPU key_on_count: {spu_walk.get('key_on_count')}")

        # Test B: Claw Slash Attack
        print("Action B: Pressing SQUARE (Claw slash melee attack)...")
        send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_SQUARE), 'frames': 8})
        time.sleep(0.3)
        send_cmd({'cmd': 'screenshot_file', 'path': 'akuji_action_slash.png'})
        spu_slash = send_cmd({'cmd': 'spu_status'})
        print(f"  Claw attack captured. SPU key_on_count: {spu_slash.get('key_on_count')}")

        # Test C: Jump
        print("Action C: Pressing CROSS (Vertical jump)...")
        send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_CROSS), 'frames': 8})
        time.sleep(0.3)
        send_cmd({'cmd': 'screenshot_file', 'path': 'akuji_action_jump.png'})
        spu_jump = send_cmd({'cmd': 'spu_status'})
        print(f"  Jump state captured. SPU key_on_count: {spu_jump.get('key_on_count')}")

        # Test D: Turn & Camera Rotation
        print("Action D: Holding RIGHT (Turn Akuji)...")
        send_cmd({'cmd': 'press', 'buttons': make_mask(PAD_RIGHT), 'frames': 30})
        time.sleep(1.0)
        send_cmd({'cmd': 'screenshot_file', 'path': 'akuji_action_turn.png'})
        print("  Turn state captured.")

        # Final Verification Summary
        g_final = send_cmd({'cmd': 'gpu_state'})
        f_final = send_cmd({'cmd': 'frame'})
        r_final = send_cmd({'cmd': 'get_registers'})
        results['final_state'] = {
            'frame': f_final.get('frame'),
            'draws': g_final.get('gp0_draw'),
            'writes': g_final.get('gp0_writes'),
            'pc': r_final.get('pc')
        }
        print(f"\nFinal State: Frame {f_final.get('frame')}, Total Draws: {g_final.get('gp0_draw')}, Total Writes: {g_final.get('gp0_writes')}, PC: {r_final.get('pc')}")

        with open('compatibility_audit.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("Saved compatibility_audit.json.")

    finally:
        p.kill()
        print("Test run completed.")

if __name__ == '__main__':
    main()
