from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

hash_context = PasswordHash((Argon2Hasher(),))
def hash_password(password: str) -> str:
    """ Convert plain password to hash password """
   
    return hash_context.hash(password)
    
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verify whether the password match with the hash """
    return hash_context.verify(plain_password,hashed_password)
