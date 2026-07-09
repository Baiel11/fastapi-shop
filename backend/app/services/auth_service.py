from sqlalchemy.orm import Session
from jose import JWTError

from ..repositories.user_repository import UserRepository
from ..schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from ..core.passwords import hash_password, verify_password
from ..core.jwt import create_access_token, create_refresh_token, decode_token
from ..core.exceptions import ConflictException, UnauthorizedException, ForbiddenException

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register(self, data: UserRegister) -> UserResponse:
        if self.user_repo.get_by_email(data.email):
            raise ConflictException(detail="Email already registered")
        
        if self.user_repo.get_by_username(data.username):
            raise ConflictException(detail="Username already taken")
        
        # Hash happens here
        hashed = hash_password(data.password)
        user = self.user_repo.create(
            email=data.email,
            username=data.username,
            hashed_password=hashed
        )

        return UserResponse.model_validate(user)
    
    def login(self, data: UserLogin) -> TokenResponse:
        user = self.user_repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException(detail="Invalid email or password")
        
        if not user.is_active:
            raise ForbiddenException(detail="Account is disabled")
        
        payload = {"sub": str(user.id)}
        return TokenResponse(
            access_token=create_access_token(payload),
            refresh_token=create_refresh_token(payload)
        )
    
    def get_user_by_token(self, token: str) -> UserResponse:
        try:
            payload = decode_token(token)
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type")

            if user_id is None or token_type != "access":
                raise UnauthorizedException(detail="Invalid token")
        except JWTError:
            raise UnauthorizedException(detail="Invalid or expired token")
        
        user = self.user_repo.get_by_id(int(user_id))
        if not user:
            raise UnauthorizedException(detail="User not found")
        
        return UserResponse.model_validate(user)