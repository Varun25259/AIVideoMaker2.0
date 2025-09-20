from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
def make_thumbnail(title, lang='en'):
    thumb = Image.new('RGB', (1280,720), color=(25,25,112))
    draw = ImageDraw.Draw(thumb)
    fnt = ImageFont.load_default()
    draw.text((60,260), title, font=fnt, fill=(255,255,255))
    out = Path(__file__).parent.parent / 'output_videos' / f'thumb_{title[:30].replace(' ','_')}.jpg'
    out.parent.mkdir(parents=True, exist_ok=True)
    thumb.save(out)
    return str(out)
