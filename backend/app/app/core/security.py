from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet, InvalidToken
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class ExpiringActivateTokenGenerator:
  fernet = Fernet(str.encode("xPNRNf6LInjPFQuguVxrQEZwsaTJyA-YstXMFlH1ujY="))
  DATE_FORMAT = '%Y-%m-%d %H-%M-%S'
  EXPIRATION_DAYS = 3

  def _get_time(self):
    """Returns a string with the current UTC time"""
    return datetime.utcnow().strftime(self.DATE_FORMAT)

  def _parse_time(self, d):
    """Parses a string produced by _get_time and returns a datetime object"""
    return datetime.strptime(d, self.DATE_FORMAT)

  def generate_token(self, text: str) -> str:
    """Generates an encrypted token"""
    full_text = text + '|' + self._get_time()
    token = self.fernet.encrypt(bytes(full_text, encoding='utf-8')).decode("utf-8") 

    return token

  def get_token_value(self, token: str) -> Union[str, None]:
    """Gets a value from an encrypted token.
    Returns None if the token is invalid or has expired.
    """
    try:
      value = self.fernet.decrypt(bytes(token, encoding='utf-8')).decode('utf-8')
      separator_pos = value.rfind('|')
      text = value[: separator_pos]
      token_time = self._parse_time(value[separator_pos + 1: ])
      
      if token_time + timedelta(self.EXPIRATION_DAYS) < datetime.utcnow():
        return None

    except InvalidToken:
      return None

    return text 

  def is_valid_token(self, token):
    return self.get_token_value(token) != None