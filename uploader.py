import os, pickle, pathlib, time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']
ROOT = pathlib.Path(__file__).parent.parent
CREDENTIALS_FILE = ROOT / 'client_secrets.json'
TOKEN_FILE = ROOT / 'youtube_token.pickle'

def get_authenticated_service():
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError('client_secrets.json not found. Create OAuth credentials in Google Cloud Console and download.')
    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as f:
            pickle.dump(creds, f)
    return build('youtube', 'v3', credentials=creds)

def list_connected_channels():
    service = get_authenticated_service()
    request = service.channels().list(part='id,snippet', mine=True)
    resp = request.execute()
    channels = [f"{item['snippet'].get('title')} ({item['id']})" for item in resp.get('items',[])]
    return service, channels

def upload_video(video_file: str, title: str, description: str = '', tags: list = None, privacyStatus: str = 'unlisted'):
    service = get_authenticated_service()
    body = {'snippet': {'title': title, 'description': description, 'tags': tags or [], 'categoryId': '22'},
            'status': {'privacyStatus': privacyStatus, 'selfDeclaredMadeForKids': False}}
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype='video/*')
    request = service.videos().insert(part='snippet,status', body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f'Upload progress: {int(status.progress()*100)}%')
    return response.get('id')

def youtube_authenticate_and_upload(video_path, title, description, tags=None, privacy='unlisted'):
    vid = upload_video(video_path, title, description, tags, privacyStatus=privacy)
    return {'videoId': vid}
