import os
import urllib

from dotenv import load_dotenv
import aiohttp


load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
DISK_APP_FOLDER = 'apps/Uploader/'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'


async def upload_file(session, file):
    """Загружает файл на Яндекс.Диск и возвращает его расположение."""
    async with session.get(
            REQUEST_UPLOAD_URL,
            headers=AUTH_HEADERS,
            params={
                'path': f'{DISK_APP_FOLDER}{file.filename}',
                'overwrite': 'True'
            },
    ) as response:
        upload_url = (await response.json())['href']

    async with session.put(data=file.read(), url=upload_url) as response:
        location = urllib.parse.unquote(response.headers['Location'])

    return location.replace('/disk', '')


async def get_url(session, location, filename):
    """Получает ссылку для скачивания файла с Яндекс.Диска."""
    async with session.get(
            DOWNLOAD_LINK_URL,
            headers=AUTH_HEADERS,
            params={'path': location},
    ) as response:
        download_url = (await response.json())['href']

    return dict(filename=filename, url=download_url)


async def upload_files_to_disk(files):
    """Загружает несколько файлов на Яндекс.Диск и возвращает ссылки на них."""
    async with aiohttp.ClientSession() as session:
        results = []
        for file in files:
            location = await upload_file(session, file)
            result = await get_url(session, location, file.filename)
            results.append(result)
        return results