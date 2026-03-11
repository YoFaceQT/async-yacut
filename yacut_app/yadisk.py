import os
import urllib

import aiohttp
import asyncio
from dotenv import load_dotenv


load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
DISK_APP_FOLDER = 'apps/Uploader/'


async def upload_files_to_disk(files):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[upload_file_and_get_url(session, file) for file in files]
        )


async def upload_file_and_get_url(session, file):
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
    location = location.replace('/disk', '')
    async with session.get(
            DOWNLOAD_LINK_URL,
            headers=AUTH_HEADERS,
            params={'path': location, },
    ) as response:
        download_url = (await response.json())['href']
    return dict(filename=file.filename, url=download_url)
