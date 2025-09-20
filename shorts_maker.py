from pathlib import Path
def extract_shorts(video_path):
    out_dir = Path(__file__).parent.parent / 'output_videos'
    out_dir.mkdir(exist_ok=True)
    fake_shorts = [str(out_dir / 'short_'+str(i)+'.mp4') for i in range(1,4)]
    for p in fake_shorts:
        Path(p).write_text('placeholder for short clip')  # placeholder small files
    return fake_shorts
