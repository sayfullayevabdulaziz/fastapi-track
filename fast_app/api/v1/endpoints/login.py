from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import EmailStr
from pydantic import ValidationError

from fast_app import crud
from fast_app.api import deps
from fast_app.core import security
from fast_app.core.config import settings
from fast_app.core.security import get_password_hash
from fast_app.core.security import verify_password
from fast_app.models.user_model import User
from fast_app.schemas.common_schema import MetaGeneral
from fast_app.schemas.response_schema import PostResponseBase, create_response
from fast_app.schemas.token_schema import TokenRead, Token, RefreshToken
from fast_app.utils.send_email import send_email_async

router = APIRouter()


@router.post("")
async def login(
    email: EmailStr = Body(...),
    password: str = Body(...),
    meta_data: MetaGeneral = Depends(deps.get_general_meta)
) -> PostResponseBase[Token]:
    """
    Login for all users
    """
    user = await crud.user.authenticate(email=email, password=password)
    if not user:
        raise HTTPException(status_code=400, detail={"message": "Email or Password incorrect", "status": 0})
    elif not user.is_active:
        raise HTTPException(status_code=400, detail={"message": "User is inactive", "status": 0})
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(
        user.id, expires_delta=refresh_token_expires
    )
    data = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user=user,
    )

    return create_response(meta=meta_data, data=data, message="Login correctly")


@router.post("/forgot-password-by-email")
async def email_check(
        email: EmailStr = Body(...)
):
    user = await crud.user.get_by_email(email=email)

    if not user:
        raise HTTPException(status_code=400, detail="Email incorrect")

    await send_email_async('Hello World', 'saa13122002@gmail.com',
                           {'title': 'Hello World', 'name': 'John Doe'})
    return 'Success'


@router.post("/change_password")
async def change_password(
    current_password: str = Body(...),
    new_password: str = Body(...),
    current_user: User = Depends(deps.get_current_user())
) -> PostResponseBase[Token]:
    """
    Change password
    """

    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Current Password")

    if verify_password(new_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="New Password should be different that the current one",
        )

    new_hashed_password = get_password_hash(new_password)
    await crud.user.update(
        obj_current=current_user, obj_new={"hashed_password": new_hashed_password}
    )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        current_user.id, expires_delta=access_token_expires
    )
    refresh_token = security.create_refresh_token(
        current_user.id, expires_delta=refresh_token_expires
    )
    data = Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token,
        user=current_user,
    )

    return create_response(data=data, message="New password generated")


@router.post("/new_access_token", status_code=201)
async def get_new_access_token(
    body: RefreshToken = Body(...)
) -> PostResponseBase[TokenRead]:
    """
    Gets a new access token using the refresh token  for future requests
    """
    try:
        payload = jwt.decode(
            body.refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )

    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Refresh token invalid")

    if payload["type"] != "refresh":
        raise HTTPException(status_code=404, detail="Incorrect token")
    user_id = int(payload["sub"])
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    user = await crud.user.get(id=user_id)
    if user.is_active:
        access_token = security.create_access_token(
            payload["sub"], expires_delta=access_token_expires
        )
        return create_response(
            data=TokenRead(access_token=access_token, token_type="bearer"),
            message="Access token generated correctly",
        )
    else:
        raise HTTPException(status_code=404, detail="User inactive")


@router.post("/access-token")
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenRead:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await crud.user.authenticate(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }