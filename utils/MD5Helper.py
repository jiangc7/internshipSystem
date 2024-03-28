import hashlib


def md5_encrypt(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def check_match(passwordFromDB, passwordFromWeb):
    if passwordFromDB == md5_encrypt(passwordFromWeb):
        return True
    return False
