MAX_CUSTOM_ID_LENGTH = 16
DEFAULT_SHORT_ID_LENGTH = 6

ALLOWED_SYMBOLS = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789'
)

SHORT_ID_PATTERN = r'^[A-Za-z0-9]*$'

INVALID_NAME_MESSAGE = 'Указано недопустимое имя для короткой ссылки'

NO_BODY_MESSAGE = 'Отсутствует тело запроса'

NO_URL_MESSAGE = '"url" является обязательным полем!'

NOT_FOUND_MESSAGE = 'Указанный id не найден'

DUPLICATE_MESSAGE = 'Предложенный вариант короткой ссылки уже существует.'

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
