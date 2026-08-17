# from DTOs.user_info_dto import UserInfoDTO
# from core.functions.jwt import decode_access_token 
# from fastapi import Depends
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# security = HTTPBearer()

# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
# ) -> UserInfoDTO:
#     """تستخرج التوكين الممرر يدوياً وتتحقق منه"""
#     token = credentials.credentials  # النص الخاص بالـ Token فقط
#     user_dto = decode_access_token(token)
#     return user_dto