from passlib.context import CryptContext # For Hashing


pwd_context = CryptContext(schemes=['bcrypt'],deprecated = "auto")


def hash(password : str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password,hashed_password)