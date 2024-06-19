from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)
