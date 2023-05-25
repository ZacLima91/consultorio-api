from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'],)


def gerate_hash(txt):
    return pwd_context.hash(txt)


def verify_hash(txt, hash):
    return pwd_context.verify(txt, hash)