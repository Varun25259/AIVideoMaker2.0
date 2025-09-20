import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TMP = Path(__file__).parent.parent / 'tmp'
TMP.mkdir(exist_ok=True)

def assemble_basic_mp4(broll_path: str, voice_path: str, out_path: str):
    cmd = ['ffmpeg', '-y', '-i', broll_path, '-i', voice_path, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-c:a', 'aac', '-shortest', out_path]
    subprocess.run(cmd, check=True)
    return out_path

def create_thumbnail(title, lang='en'):
    thumb = Image.new('RGB', (1280,720), color=(30,30,30))
    draw = ImageDraw.Draw(thumb)
    fnt = ImageFont.load_default()
    draw.text((50,300), title, font=fnt, fill=(255,255,255))
    out = Path(__file__).parent.parent / 'output_videos' / f'thumb_{title[:30].replace(" ","_")}.jpg'
    out.parent.mkdir(parents=True, exist_ok=True)
    thumb.save(out)
    return str(out)
