from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.config import settings

# Contexto para hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Cria um hash da senha"""
    if not password or len(password) < 6:
        raise ValueError('Senha deve ter pelo menos 6 caracteres')
    
    # Truncar a senha para 72 bytes (limite do bcrypt)
    # Isso evita erros do bcrypt
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncar de forma segura, removendo bytes do final
        password_bytes = password_bytes[:72]
        # Tentar decodificar, se falhar, remover mais bytes
        while password_bytes:
            try:
                password = password_bytes.decode('utf-8')
                break
            except UnicodeDecodeError:
                password_bytes = password_bytes[:-1]
    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    # Aplicar o mesmo truncamento ao verificar
    password_bytes = plain_password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
        while password_bytes:
            try:
                plain_password = password_bytes.decode('utf-8')
                break
            except UnicodeDecodeError:
                password_bytes = password_bytes[:-1]
    
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decodifica um token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
