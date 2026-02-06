from pwdlib import PasswordHash



password_hash = PasswordHash.recommended()
class Hash():
    def bcrypt(password: str):
        return password_hash.hash(password)
    def verifypassword(hashed_password: str, password: str):
        return password_hash.verify(hashed_password, password)