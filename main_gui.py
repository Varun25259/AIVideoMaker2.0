"""AI Video Maker - Upgraded Full Version (Source)
Main GUI provides access to advanced modules. Many advanced features are provided as safe stubs
that you can later replace with production integrations (voice-clone, social posting, offline models).
"""
import os, sys, traceback
from pathlib import Path
import PySimpleGUI as sg
from scriptgen import generate_script
from tts_elevenlabs import text_to_speech_eleven
from video_builder import assemble_basic_mp4, create_thumbnail
from uploader import list_connected_channels, youtube_authenticate_and_upload
from thumbnailer import make_thumbnail
from shorts_maker import extract_shorts
from translator import translate_text
from social_poster_stub import post_to_twitter_stub, post_to_facebook_stub
from voice_clone import clone_voice_from_samples_stub
from self_upgrade_stub import propose_self_upgrade, run_self_upgrade_stub
from admin_dashboard_stub import open_admin_dashboard_stub
from error_handler import safe_run

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output_videos"
OUTPUT_DIR.mkdir(exist_ok=True)

sg.theme('LightGreen')

layout = [
    [sg.Text('AI Video Maker — Upgraded', font=('Helvetica',18)), sg.Text('', key='-STATUS-', size=(40,1))],
    [sg.TabGroup([[
        sg.Tab('Setup', [
            [sg.Text('OpenAI API Key:'), sg.Input(key='-OPENAI-')],
            [sg.Text('ElevenLabs API Key:'), sg.Input(key='-ELEVEN-')],
            [sg.Text('Encryption Passphrase:'), sg.Input(key='-PASS-', password_char='*')],
            [sg.Button('Save Keys'), sg.Button('Load Keys')],
            [sg.HorizontalSeparator()],
            [sg.Text('YouTube OAuth:'), sg.Button('Connect YouTube'), sg.Text('', key='-YT-')],
            [sg.Text("Note: Do not upload keys to Github. Keep client_secrets.json local for OAuth.")]
        ]),
        sg.Tab('Generate', [
            [sg.Text('Topic/Keyword:'), sg.Input(key='-TOPIC-', size=(50,1)), sg.Combo(['Hindi','English','Spanish'], default_value='Hindi', key='-LANG-')],
            [sg.Text('Length:'), sg.Combo(['short','medium','long'], default_value='medium', key='-LEN-'), sg.Text('Videos/day:'), sg.Input('1', key='-LIMIT-', size=(6,1))],
            [sg.Button('Generate Now (local)'), sg.Button('Generate & Upload'), sg.Button('Generate, Post & Schedule')],
            [sg.Text('Advanced Options:'), sg.Checkbox('Create Shorts', key='-SHORTS-'), sg.Checkbox('Auto-translate', key='-TRANSLATE-')],
            [sg.Multiline('', size=(90,12), key='-LOG-')]
        ]),
        sg.Tab('Channels', [
            [sg.Text('Connected Channels:'), sg.Listbox(values=[], size=(60,6), key='-CHANLIST-')],
            [sg.Button('Refresh Channels'), sg.Button('Open Output Folder')]
        ]),
        sg.Tab('Advanced', [
            [sg.Button('Voice Clone (Train Stub)'), sg.Button('Self-Upgrade (Propose)'), sg.Button('Run Approved Upgrade (Stub)')],
            [sg.Button('Admin Dashboard'), sg.Button('Post to Social (Stub)')],
            [sg.Text('Experimental features are placeholders — enable only after review.')]
        ])
    ]])]
]

window = sg.Window('AI Video Maker - Upgraded', layout, finalize=True, resizable=True)

def log(msg):
    cur = window['-LOG-'].get()
    window['-LOG-'].update(cur + msg + '\n')

while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
    try:
        if event == 'Save Keys':
            p = values['-PASS-'].strip()
            if not p:
                sg.popup('Provide a passphrase for secure storage.')
            else:
                from security import save_keys_securely
                save_keys_securely({'OPENAI': values['-OPENAI-'].strip(), 'ELEVEN': values['-ELEVEN-'].strip()}, p)
                sg.popup('Keys saved locally (encrypted).')
        if event == 'Load Keys':
            p = values['-PASS-'].strip()
            if not p:
                sg.popup('Enter passphrase to load keys.')
            else:
                from security import load_keys_securely
                data = load_keys_securely(p)
                if data:
                    window['-OPENAI-'].update(data.get('OPENAI',''))
                    window['-ELEVEN-'].update(data.get('ELEVEN',''))
                    sg.popup('Keys loaded into fields.')
                else:
                    sg.popup('No saved keys found.')
        if event == 'Connect YouTube':
            window['-YT-'].update('Connecting...')
            try:
                service, channels = list_connected_channels()
                window['-CHANLIST-'].update(channels)
                window['-YT-'].update('Connected')
                log('YouTube connected.')
            except Exception as e:
                window['-YT-'].update('Not connected')
                log('YouTube connect error:' + str(e))
        if event == 'Generate Now (local)':
            topic = values['-TOPIC-'].strip() or 'Sample Topic'
            lang = values['-LANG-']
            log('Generating script...')
            script = safe_run(lambda: generate_script(topic, language=lang), log=log)
            log('Generating voice...')
            audio = safe_run(lambda: text_to_speech_eleven(script), log=log)
            log('Creating thumbnail...')
            thumb = safe_run(lambda: make_thumbnail(topic, lang), log=log)
            broll = PROJECT_ROOT / 'sample.mp4'
            if not broll.exists():
                log('No sample.mp4 found in project root; add one to test assemble.')
                continue
            outfn = OUTPUT_DIR / f"{topic[:30].replace(' ','_')}_{lang}_{int(datetime.datetime.now().timestamp())}.mp4"
            out = safe_run(lambda: assemble_basic_mp4(str(broll), audio, str(outfn)), log=log)
            log(f'Video created: {out}')
            if values['-SHORTS-']:
                log('Extracting shorts...')
                shorts = safe_run(lambda: extract_shorts(str(out)), log=log)
                log('Shorts: ' + str(shorts))
            if values['-TRANSLATE-']:
                log('Translating script...')
                t = safe_run(lambda: translate_text(script, target_langs=['en','hi','es']), log=log)
                log('Translations: ' + str(list(t.keys())))
            sg.popup('Local generation complete.', str(out))
        if event == 'Generate & Upload':
            topic = values['-TOPIC-'].strip() or 'Upload Topic'
            script = generate_script(topic, language=values['-LANG-'])
            audio = text_to_speech_eleven(script)
            broll = PROJECT_ROOT / 'sample.mp4'
            if not broll.exists():
                log('No sample.mp4 found.')
                continue
            outfn = OUTPUT_DIR / f"{topic[:30].replace(' ','_')}_{values['-LANG-']}.mp4"
            assemble_basic_mp4(str(broll), audio, str(outfn))
            try:
                res = youtube_authenticate_and_upload(str(outfn), title=topic, description='Auto-generated', tags=['AI','auto'])
                log('Uploaded video id: ' + str(res.get('videoId')))
            except Exception as e:
                log('Upload failed: ' + str(e))
        if event == 'Generate, Post & Schedule':
            # Generate, upload, and post to social (stubs)
            topic = values['-TOPIC-'].strip() or 'Auto Post Topic'
            script = generate_script(topic, language=values['-LANG-'])
            audio = text_to_speech_eleven(script)
            broll = PROJECT_ROOT / 'sample.mp4'
            if not broll.exists():
                log('No sample.mp4 found.')
                continue
            outfn = OUTPUT_DIR / f"{topic[:30].replace(' ','_')}_{values['-LANG-']}.mp4"
            assemble_basic_mp4(str(broll), audio, str(outfn))
            try:
                res = youtube_authenticate_and_upload(str(outfn), title=topic, description='Auto-generated', tags=['AI','auto'])
                log('Uploaded: ' + str(res.get('videoId')))
                # social posts (stubs)
                post_to_twitter_stub(outfn, f"New video: {topic}")
                post_to_facebook_stub(outfn, f"Check this out: {topic}")
                log('Posted to social (stubs).')
            except Exception as e:
                log('Upload/Post failed: ' + str(e))
        if event == 'Refresh Channels':
            try:
                service, channels = list_connected_channels()
                window['-CHANLIST-'].update(channels)
                log('Channels refreshed.')
            except Exception as e:
                log('Refresh failed: ' + str(e))
        if event == 'Open Output Folder':
            os.startfile(str(OUTPUT_DIR))
        if event == 'Voice Clone (Train Stub)':
            sg.popup('Voice clone is experimental. This will only run a local stub.')
            clone_voice_from_samples_stub()
            log('Voice clone stub invoked.')
        if event == 'Self-Upgrade (Propose)':
            summary = propose_self_upgrade()
            log('Proposed self-upgrade: ' + str(summary))
            sg.popup('Self-upgrade proposed. Review in Admin Dashboard.')
        if event == 'Run Approved Upgrade (Stub)':
            sg.popup('Running approved upgrade (stub).')
            run_self_upgrade_stub()
            log('Ran approved upgrade (stub).')
        if event == 'Admin Dashboard':
            open_admin_dashboard_stub()
            log('Admin dashboard opened (stub).')
        if event == 'Post to Social (Stub)':
            sg.popup('Posting to social networks using stubs.')
            # Example: call post stubs with placeholders
            post_to_twitter_stub('','Test post from AI Video Maker')
            log('Posted to social (stubs).')
    except Exception as e:
        traceback.print_exc()
        log('Error: ' + str(e))

window.close()
