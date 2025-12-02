"""
Google OAuth2 Authentication Module
Free-tier authentication with Google using FastAPI
Team ID: Auto-250358
"""

import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Configuration - All FREE tier services
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

JWT_SECRET = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

class UserProfile(BaseModel):
    """Google user profile information"""
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    email_verified: bool = False
    locale: Optional[str] = None

class TokenResponse(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfile

class GoogleOAuthHandler:
    """Handle Google OAuth2 authentication - FREE TIER"""
    
    @staticmethod
    def get_authorization_url() -> str:
        """Generate Google OAuth authorization URL"""
        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",  # For refresh tokens if needed
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    
    @staticmethod
    async def exchange_code_for_token(code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token - FREE TIER"""
        async with httpx.AsyncClient() as client:
            data = {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": GOOGLE_REDIRECT_URI,
            }
            
            try:
                response = await client.post(GOOGLE_TOKEN_URL, data=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error exchanging code: {e}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to exchange authorization code"
                )
    
    @staticmethod
    async def get_user_info(access_token: str) -> UserProfile:
        """Get user information from Google - FREE TIER"""
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {access_token}"}
            
            try:
                response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
                response.raise_for_status()
                user_data = response.json()
                
                return UserProfile(
                    user_id=user_data.get("sub"),
                    email=user_data.get("email"),
                    name=user_data.get("name"),
                    picture=user_data.get("picture"),
                    email_verified=user_data.get("email_verified", False),
                    locale=user_data.get("locale"),
                )
            except httpx.HTTPError as e:
                logger.error(f"Error fetching user info: {e}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Failed to fetch user information"
                )
    
    @staticmethod
    def create_jwt_token(user: UserProfile) -> str:
        """Create JWT token for user session"""
        payload = {
            "sub": user.user_id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    @staticmethod
    def verify_jwt_token(token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

# Initialize handler
oauth_handler = GoogleOAuthHandler()src/utils/auth.py
