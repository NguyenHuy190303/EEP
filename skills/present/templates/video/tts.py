"""One sentence per line -> per-line AIFF via macOS `say`, timeline.json, narration.wav, .srt.
usage: python3 tts.py <script.txt> <outprefix> [--voice Daniel] [--gap 0.45] [--lead 0.6] [--tail 1.2]"""
import argparse, json, subprocess, tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("script"); ap.add_argument("out")
ap.add_argument("--voice", default="Daniel"); ap.add_argument("--rate", type=int, default=175)
ap.add_argument("--gap", type=float, default=0.45); ap.add_argument("--lead", type=float, default=0.6)
ap.add_argument("--tail", type=float, default=1.2)
a = ap.parse_args()
lines = [l.strip() for l in Path(a.script).read_text().splitlines() if l.strip()]
tmp = Path(tempfile.mkdtemp())
SR = 48000

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

def silence(sec, p):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{sec:.3f}", str(p)], check=True)

parts, cues, t = [], [], a.lead
silence(a.lead, tmp / "lead.wav"); parts.append(tmp / "lead.wav")
for i, line in enumerate(lines):
    aiff, wav = tmp / f"s{i}.aiff", tmp / f"s{i}.wav"
    subprocess.run(["say", "-v", a.voice, "-r", str(a.rate), "-o", str(aiff), line], check=True)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-i", str(aiff), "-ar", str(SR), "-ac", "1", str(wav)], check=True)
    d = dur(wav)
    cues.append({"i": i, "start": round(t, 3), "end": round(t + d, 3), "text": line})
    parts.append(wav); t += d
    g = tmp / f"g{i}.wav"; gap = a.tail if i == len(lines) - 1 else a.gap
    silence(gap, g); parts.append(g); t += gap
lst = tmp / "list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", f"{a.out}.wav"], check=True)
Path(f"{a.out}.timeline.json").write_text(json.dumps({"voice": a.voice, "total": round(t, 3), "cues": cues}, indent=1))

def ts(x):
    ms = int(round(x * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
Path(f"{a.out}.srt").write_text("".join(f"{c['i']+1}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text']}\n\n" for c in cues))
print(f"{a.out}: {len(cues)} cues, {t:.2f}s, voice={a.voice}")
