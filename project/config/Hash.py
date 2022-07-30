from werkzeug.security import check_password_hash, generate_password_hash
from hashlib import md5

class Hash:

    def __init__(self):
        pass

    def cekHash(self, pwhash, password):
        return check_password_hash(pwhash, password)

    def getHash(self, password):
        return generate_password_hash(password)
    
    def md5(self, text):
        return md5(text).hexdigest()
