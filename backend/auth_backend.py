"""
Sistema de autenticación para AutoTest
- Registro de usuarios
- Login con JWT
- Validación de sesiones
- Protección de rutas
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
import secrets

from database import get_db
from models_auth import Usuario

# Configuración de seguridad
SECRET_KEY = secrets.token_urlsafe(32)  # En producción, usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

# Configuración de password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


# ============================================================================
# SCHEMAS DE AUTENTICACIÓN
# ============================================================================

class UsuarioRegistro(BaseModel):
    """Schema para registro de nuevo usuario"""
    email: EmailStr
    username: str
    password: str
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    
    @validator('username')
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError('El username debe tener al menos 3 caracteres')
        if not v.isalnum() and '_' not in v:
            raise ValueError('El username solo puede contener letras, números y guiones bajos')
        return v
    
    @validator('password')
    def password_strong(cls, v):
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v


class UsuarioLogin(BaseModel):
    """Schema para login"""
    username: str
    password: str


class Token(BaseModel):
    """Schema para token JWT"""
    access_token: str
    token_type: str
    user: dict


class UsuarioResponse(BaseModel):
    """Schema para respuesta de usuario"""
    id: int
    email: str
    username: str
    nombre: Optional[str]
    apellidos: Optional[str]
    is_verified: bool
    created_at: datetime
    chatbot_limite_diario: int
    
    class Config:
        from_attributes = True
        populate_by_name = True
    
    @classmethod
    def from_usuario(cls, usuario):
        return cls(
            id=usuario.id,
            email=usuario.email,
            username=usuario.username,
            nombre=usuario.nombre,
            apellidos=usuario.apellidos,
            is_verified=usuario.is_verified,
            created_at=usuario.created_at,
            chatbot_limite_diario=usuario.chatbot_preguntas_dia
        )


class CambioPassword(BaseModel):
    """Schema para cambio de contraseña"""
    password_actual: str
    password_nueva: str
    
    @validator('password_nueva')
    def password_strong(cls, v):
        if len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    # Bcrypt tiene un límite de 72 bytes, truncamos si es necesario
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Genera hash de contraseña"""
    # Bcrypt tiene un límite de 72 bytes, truncamos si es necesario
    if isinstance(password, str):
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_usuario_by_username(db: Session, username: str) -> Optional[Usuario]:
    """Obtiene usuario por username"""
    return db.query(Usuario).filter(Usuario.username == username).first()


def get_usuario_by_email(db: Session, email: str) -> Optional[Usuario]:
    """Obtiene usuario por email"""
    return db.query(Usuario).filter(Usuario.email == email).first()


def autenticar_usuario(db: Session, username: str, password: str) -> Optional[Usuario]:
    """Autentica usuario con username y password"""
    usuario = get_usuario_by_username(db, username)
    if not usuario:
        return None
    if not verify_password(password, usuario.password_hash):
        return None
    return usuario


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[Usuario]:
    """
    Obtiene el usuario actual desde el token JWT
    Retorna None si no hay token o es inválido (permite acceso anónimo)
    """
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
    except JWTError:
        return None
    
    usuario = get_usuario_by_username(db, username)
    return usuario


async def get_current_user_required(
    current_user: Optional[Usuario] = Depends(get_current_user)
) -> Usuario:
    """
    Obtiene el usuario actual y requiere que esté autenticado
    Lanza excepción 401 si no está autenticado
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Por favor inicie sesión.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    return current_user


# ============================================================================
# ENDPOINTS DE AUTENTICACIÓN
# ============================================================================

def registrar_usuario(registro: UsuarioRegistro, db: Session) -> Usuario:
    """
    Registra un nuevo usuario en el sistema
    """
    # Verificar si el email ya existe
    if get_usuario_by_email(db, registro.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el username ya existe
    if get_usuario_by_username(db, registro.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso"
        )
    
    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        email=registro.email,
        username=registro.username,
        password_hash=get_password_hash(registro.password),
        nombre=registro.nombre,
        apellidos=registro.apellidos,
        is_active=True,
        is_verified=False,  # Podría requerir verificación por email
        chatbot_preguntas_dia=20  # Límite para usuarios registrados
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario


def login_usuario(form_data: OAuth2PasswordRequestForm, db: Session) -> dict:
    """
    Autentica usuario y retorna token JWT
    """
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    
    # Actualizar último login
    usuario.last_login = datetime.utcnow()
    db.commit()
    
    # Crear token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": usuario.to_dict()
    }


def cambiar_password(
    cambio: CambioPassword,
    current_user: Usuario,
    db: Session
) -> dict:
    """
    Cambia la contraseña del usuario actual
    """
    # Verificar contraseña actual
    if not verify_password(cambio.password_actual, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    
    # Actualizar contraseña
    current_user.password_hash = get_password_hash(cambio.password_nueva)
    db.commit()
    
    return {"message": "Contraseña actualizada correctamente"}
