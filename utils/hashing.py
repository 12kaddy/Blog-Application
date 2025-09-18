from passlib.context import CryptContext
from app.core.config.settings import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    # Production-grade parameters
    bcrypt__rounds=settings.PASSWORD_HASH_ROUNDS or 12,
    bcrypt__ident="2b"
)

def hash_password(password: str) -> str:
    """
    Securely hashes passwords using:
    - Per-user salts
    - Configurable work factor
    - Modern bcrypt version (2b)
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Constant-time verification to prevent timing attacks
    Automatically handles hash version upgrades
    """
    return pwd_context.verify(plain_password, hashed_password)

def needs_rehash(hashed_password: str) -> bool:
    """
    Check if password needs rehashing due to:
    - Algorithm upgrades
    - Work factor changes
    """
    return pwd_context.needs_update(hashed_password)