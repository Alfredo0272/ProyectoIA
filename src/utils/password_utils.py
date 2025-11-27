import bcrypt

def hash_password(password: str) -> str:
  salt = bcrypt.gensalt(12)
  hased = bcrypt.hashpw(password.encode('utf-8'),salt)
  return hased.decode('utf-8')

def veryfy_password (hashed_password: str, password: str) -> bool:
  return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

