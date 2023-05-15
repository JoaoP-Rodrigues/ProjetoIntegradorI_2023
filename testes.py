import hashlib

password = 'JpR18091986*'
hash_object = hashlib.sha256(password.encode())
hex_dig = hash_object.hexdigest()
print(hex_dig)
