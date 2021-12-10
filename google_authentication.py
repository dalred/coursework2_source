import pickle, os, io, json
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from googleapiclient.discovery import build

def credentials():
    cred = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            cred = pickle.load(token)
    return cred

creds_google = credentials()
service = build('drive', 'v3', credentials=creds_google)

def read_google_json(file_id):
    encoding = 'utf-8'
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}")
    file_data = fh.getvalue().decode(encoding)
    data = json.loads(file_data)
    return data

def add_json_file(data, file_id):
    encoding = 'utf-8'
    json_dumps = json.dumps(data, indent=4, ensure_ascii=False).encode(encoding)
    data = io.BytesIO(json_dumps)
    media_body = MediaIoBaseUpload(data, mimetype='application/json', resumable=True)
    updated_file = service.files().update(
        fileId=file_id,
        media_body=media_body).execute()
    return updated_file

