import os


FILES_URL = 'files'
FORBIDEN_URLS = (FILES_URL,)
MAX_SHORT_URL_LENGTH = 16
MIN_SHORT_URL_LENGTH = 1
SHORT_PATTERN = '^[A-Za-z0-9]+$'
URL_MAX_LENGHT = 256
DISK_TOKEN = os.environ.get('DISK_TOKEN')
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
DISK_APP_FOLDER = 'apps/Uploader/'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'