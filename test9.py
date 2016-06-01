import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import base64
import math
random_generator = Random.new().read
key = RSA.generate(1024, random_generator) #generate pub and priv key
key2 = key
chunk_size = 128.0
publickey = key.publickey() # pub key export for exchange
f = open("C:\\WWW.YIFY-TORRENTS.COM.jpg", 'rb')
content = base64.b64encode(f.read())
print content
encrypted = []
counter = 0
for i in xrange(int(math.ceil(len(content) / chunk_size)) - 1):
    encrypted.append(publickey.encrypt(content[int(chunk_size) * i: int(chunk_size)* (i + 1)], 32))
    counter += 1
encrypted.append(publickey.encrypt(content[int(chunk_size) * counter:], 32))
    #message to encrypt is in the above line 'encrypt this message'

print 'encrypted message:', encrypted #ciphertext
f = open ('encryption.jpg', 'wb')
f.write(str(encrypted)) #write ciphertext to file
f.close()

#decrypted code below

f = open('encryption.jpg', 'rb')
message = f.read()
decrypted = ""
for i in xrange(int(math.ceil(len(content) / chunk_size))):
    decrypted += key.decrypt(ast.literal_eval(str(encrypted[i])))
print decrypted
decrypted = base64.b64decode(decrypted)
print 'decrypted', decrypted

f = open ('encryption.jpg', 'wb')
f.write(str(decrypted))
f.close()

