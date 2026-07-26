import os
from urllib.parse import unquote

import aiohttp
from dotenv import load_dotenv

from .constants import (
    DOWNLOAD_LINK_URL,
    REQUEST_UPLOAD_URL
)

load_dotenv()

DISK_TOKEN = os.getenv('DISK_TOKEN')

AUTH_HEADERS = {
    'Authorization': f'OAuth {DISK_TOKEN}'
}


async def get_upload_link(session, filename):
    response = await session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params={
            'path': f'app:/{filename}',
            'overwrite': 'True'
        }
    )

    response_data = await response.json()
    return response_data['href']


async def upload_file(session, upload_url, file):
    response = await session.put(
        upload_url,
        data=file.read()
    )

    location = response.headers['Location']
    location = unquote(location)
    location = location.replace('/disk', '')

    return location


async def get_download_link(session, path):
    response = await session.get(
        DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={
            'path': path
        }
    )

    response_data = await response.json()

    return response_data['href']


async def upload_to_disk(file):
    async with aiohttp.ClientSession() as session:
        upload_url = await get_upload_link(
            session,
            file.filename
        )

        path = await upload_file(
            session,
            upload_url,
            file
        )

        download_link = await get_download_link(
            session,
            path
        )

        return download_link
