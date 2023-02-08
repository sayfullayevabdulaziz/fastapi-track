import hashlib
import secrets
from fast_app.core.config import settings
from fastapi import UploadFile, File, HTTPException, status
from fast_app.models.image_model import ImageMediaBase
import aiofiles


async def image_save_file(images: list[UploadFile] = File(...)) -> list[ImageMediaBase]:
    image_to_db = []
    for image in images:
        try:
            FILE_PATH = f"{str(settings.BASE_DIR)}{settings.ASSETS}"
            filename = image.filename
            extension = filename.split('.')[1]

            if extension not in ['jpg', 'png']:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "File extension not allowed"})

            image_token_name = f"{secrets.token_hex(10)}.{extension}"
            generated_name = FILE_PATH + image_token_name
            file_content = await image.read()

            async with aiofiles.open(generated_name, 'wb') as f:
                await f.write(file_content)

            file_url = f"{settings.ASSETS}{image_token_name}"

            image_to_db.append(
                ImageMediaBase(
                    file_name=file_url,
                    file_content=hashlib.sha256(file_content).hexdigest(),
                    file_ext=extension
                ))
        except Exception as e:
            print(e)
            raise HTTPException(detail={"message": "Error while image uploading"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return image_to_db
