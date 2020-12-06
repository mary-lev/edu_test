import io
import json
import requests
import yadisk
import httplib2
from PIL import Image as img
import pyheif
import apiclient.discovery
from apiclient.http import MediaIoBaseDownload
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'edu_test.settings'
django.setup()

from sheets.drive_auth import httpAuth
from .models import Image

service = apiclient.discovery.build('drive', 'v3', http=httpAuth)


file_id = "12ET4D3xeOl5_BDveMz1pAvk0uPiumswb"

def get_google_file(file_id, task, student):
    file = service.files().get(fileId=file_id).execute()
    print(file['name'])
    print(file['mimeType'])

    request = service.files().get_media(fileId=file_id)
    filename = 'data/' + file['name']
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    return file

def get_just_file(file_id):
    filename = data + file_id.split('/')[-1]
    r = requests.get(file_id, allow_redirects=True)
    with open(filename, 'wb') as f:
        f.write(r.content)

def get_yandex_file(file_id):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = file_id

    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']

    download_response = requests.get(download_url)
    with open('data/1.jpg', 'wb') as f:  # Здесь укажите нужный путь к файлу
        f.write(download_response.content)


def find_folder(file_id):
    images = Image.objects.all()
    for image in images:
        if 'folder' in image.url:
            folder_id = image.url.replace(
                'https://drive.google.com/drive/folders/',
                ''
            ).replace(
                '?usp=sharing',
                ''
            ).replace(
                'https://drive.google.com/folderview?id=',
                ''
            )
            print(folder_id)
            page_token = None
            param = {}
            if page_token:
                param['pageToken'] = page_token
            children = service.files().list(
                q="{} in parents".format(folder_id),
                pageToken=page_token
                ).execute()
            for child in children.get('items', []):
                print('File Id: %s' % child['id'])

def image_download():
    images = Image.objects.all()
    for image in images:
        if 'file' in image.url:
            url = image.url.replace(
                'https://drive.google.com/file/d/',
                ''
            ).replace(
                '/view?usp=sharing',
                ''
            ).replace(
                '/view?usp=drivesdk',
                ''
            )
            try:
                data = get_google_file(url)
                image.type = data['mimeType']
                image.name = data['name']
                image.save()
            except:
                pass

images = Image.objects.filter(type='image/heif')
for image in images:
    filename = 'data/' + image.name
    heif_file = pyheif.read(filename)
    image_file = img.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    filename = filename.replace('HEIC', 'jpg')
    image.save(filename, "JPEG")