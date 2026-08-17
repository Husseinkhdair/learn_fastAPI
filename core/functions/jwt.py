# from pydantic_core import ValidationError
# from pydantic_settings import BaseSettings, SettingsConfigDict
# from datetime import datetime, timedelta, timezone
# from DTOs.user_info_dto import UserInfoDTO
# # أضف status هنا
# from fastapi import  HTTPException, status
# import jwt

# class Settings(BaseSettings):
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_DAYS: int = 5
#     REFRESH_TOKEN_EXPIRE_DAYS: int = 30

#     # ربط الكلاس بملف .env
#     model_config = SettingsConfigDict(
#         env_file=".env", env_file_encoding="utf-8"
#     )


# # إنشاء النسخة التي سيتم استدعاؤها في باقي المشروع
# settings = Settings()



# def create_access_token(
#     data: UserInfoDTO, expires_delta: timedelta | None = None
# ) -> str:
#     to_encode = data.model_dump()

#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(
#             days=settings.ACCESS_TOKEN_EXPIRE_DAYS
#         )

#     to_encode.update({"exp": expire})

#     encoded_jwt = jwt.encode(
#         to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
#     )
#     return encoded_jwt



# def decode_access_token(token: str) -> UserInfoDTO:
#     """فك تشفير الـ JWT Token وتحويل البيانات إلى UserInfoDTO"""
#     try:
#         # 1. فك تشفير التوكين باستخدام SECRET_KEY والـ ALGORITHM
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
#         )

#         # 2. تحويل الـ Dictionary إلى UserInfoDTO
#         user_dto = UserInfoDTO(**payload)
#         return user_dto

#     except jwt.ExpiredSignatureError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token has expired",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     except (jwt.InvalidTokenError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

# def create_refresh_token(
#     user_id: int, expires_delta: timedelta | None = None
# ) -> str:
#     """توليد Refresh Token يحتوي فقط على ID المستخدم ونوع التوكين"""
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(
#             days=settings.REFRESH_TOKEN_EXPIRE_DAYS
#         )

#     to_encode = {
#         "sub": str(user_id),  # معرّف المستخدم
#         "type": "refresh",  # لتمييزه عن Access Token
#         "exp": expire,
#     }

#     encoded_jwt = jwt.encode(
#         to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
#     )
#     return encoded_jwt