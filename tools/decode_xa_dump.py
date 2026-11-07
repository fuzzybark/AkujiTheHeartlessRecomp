#!/usr/bin/env python3
"""
Decode XA audio sectors from disc image to WAV.
"""
import wave
import struct

def clamp16(v):
    if v > 32767: return 32767
    if v < -32768: return -32768
    return v

def decode_xa_track(track_bin, start_lba, sector_count, out_wav):
    k0 = [0, 60, 115, 98, 122]
    k1 = [0, 0, -52, -55, -60]
    hist_l = [0, 0]
    hist_r = [0, 0]

    pcm_data = bytearray()
    audio_sectors = 0

    with open(track_bin, 'rb') as f:
        for s in range(sector_count):
            f.seek((start_lba + s) * 2352)
            raw = f.read(2352)
            if len(raw) < 2352: break
            submode = raw[18]
            channel = raw[17]
            coding = raw[19]

            if not (submode & 0x04): # Not audio
                continue
            if channel != 1:
                continue

            audio_sectors += 1
            data = raw[24:] # XA_DATA_OFFSET

            for g in range(18): # 18 sound groups
                grp = data[g*128 : (g+1)*128]
                for blk in range(4):
                    hdr_l = grp[4 + blk * 2]
                    hdr_r = grp[4 + blk * 2 + 1]
                    shift_l = max(0, 12 - (hdr_l & 0x0F))
                    shift_r = max(0, 12 - (hdr_r & 0x0F))
                    flt_l = (hdr_l >> 4) & 0x03
                    flt_r = (hdr_r >> 4) & 0x03

                    for i in range(28):
                        b = grp[16 + blk + i * 4]
                        nl = b & 0x0F
                        nr = (b >> 4) & 0x0F
                        if nl >= 8: nl -= 16
                        if nr >= 8: nr -= 16

                        sl = (nl << shift_l) + ((k0[flt_l] * hist_l[0] + k1[flt_l] * hist_l[1] + 32) >> 6)
                        sr = (nr << shift_r) + ((k0[flt_r] * hist_r[0] + k1[flt_r] * hist_r[1] + 32) >> 6)
                        sl = clamp16(sl)
                        sr = clamp16(sr)
                        hist_l[1] = hist_l[0]
                        hist_l[0] = sl
                        hist_r[1] = hist_r[0]
                        hist_r[0] = sr

                        pcm_data.extend(struct.pack('<hh', sl, sr))

    print(f"Decoded {audio_sectors} audio sectors -> {len(pcm_data)//4} frames into {out_wav}")
    with wave.open(out_wav, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(37800)
        wf.writeframes(pcm_data)

if __name__ == '__main__':
    bin_path = 'disc/Akuji the Heartless (USA) (Track 1).bin'
    # TSANIM.STR: LBA 40596, size 3215360 (1367 sectors)
    decode_xa_track(bin_path, 40596, 1367, 'tsanim_audio.wav')
    # INTRO.STR: LBA 51712, size 22528000 (9578 sectors)
    decode_xa_track(bin_path, 51712, 9578, 'intro_audio.wav')
