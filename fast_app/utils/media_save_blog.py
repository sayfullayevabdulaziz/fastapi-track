import secrets
from fast_app.core.config import settings
from fastapi import UploadFile, File, HTTPException, status
import aiofiles


async def media_save_file(media: UploadFile = File(...)) -> dict:

    FILE_PATH = f"{str(settings.BASE_DIR)}{settings.ASSETS}"
    filename = media.filename
    extension = filename.split('.')[1]

    if extension not in ['jpg', 'png', 'jpeg', 'webp', 'bmp', 'mp4',
                         'mov', 'wmv', 'avi', 'webm', 'mpeg-2', 'mkv', 'flv', 'f4v', 'swf', 'avif']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "File extension not allowed"})

    media_token_name = f"{secrets.token_hex(10)}.{extension}"
    generated_name = FILE_PATH + media_token_name
    file_content = await media.read()

    async with aiofiles.open(generated_name, 'wb') as f:
        await f.write(file_content)

    file_url = f"{settings.ASSETS}{media_token_name}"

    return {'file_name': media_token_name, 'file_url': file_url}
