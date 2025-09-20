import os, requests, time
from pathlib import Path
ELEVEN_KEY = os.environ.get('ELEVENLABS_API_KEY')
OUTDIR = Path(__file__).parent.parent / 'tmp'
OUTDIR.mkdir(exist_ok=True)

def text_to_speech_eleven(text: str, voice: str = 'alloy'):
    if not ELEVEN_KEY:
        raise RuntimeError('ELEVENLABS_API_KEY not set in environment.')
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice}'
    headers = {'xi-api-key': ELEVEN_KEY, 'Content-Type':'application/json'}
    data = {'text': text, 'voice_settings': {'stability':0.6,'similarity_boost':0.6}}
    with requests.post(url, headers=headers, json=data, stream=True, timeout=120) as r:
        if r.status_code not in (200,201):
            raise RuntimeError(f'ElevenLabs TTS failed: {r.status_code} {r.text}')
        out = OUTDIR / f'voice_{int(time.time())}.mp3'
        with open(out, 'wb') as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
    return str(out)
