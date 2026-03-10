import os
import requests
from dotenv import load_dotenv

# load_dotenv()
# DISK_TOKEN = os.environ.get('DISK_TOKEN')
DISK_TOKEN='y0__xCzwZYeGNuWAyD6xMXZFlooy553AAenv1BKnUZFvzKKIhfz'

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'

AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}


def upload_file_to_disk(file):

    filename = file.filename
    disk_path = f'apps/Uploader/{filename}'
    upload_url = get_upload_url(disk_path)
    upload_file(file, upload_url)

    download_link = get_download_link(disk_path)
    return {
        'filename': filename,
        'download_link': download_link,
        'success': True
    }


def get_upload_url(disk_path):
    payload = {
        'path': disk_path,
        'overwrite': 'true'
    }

    response = requests.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    )

    response.raise_for_status()
    return response.json()['href']


def upload_file(file, upload_url):
    file_data = file.read()

    response = requests.put(
        data=file_data,
        url=upload_url
    )

    response.raise_for_status()
    file.seek(0)


def get_download_link(disk_path):

    response = requests.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': disk_path}
    )

    response.raise_for_status()
    print(response.json()['href'])
    return response.json()['href']


def upload_files_to_disk(files):
    results = []

    for file in files:
        result = upload_file_to_disk(file)
        results.append(result)
        print(f"Загружен файл: {file.filename}, успешно: {result['success']}")

    return results